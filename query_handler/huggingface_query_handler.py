
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain import HuggingFaceHub, PromptTemplate
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory


import logging

# Loading API Keys
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]


class LLMQueryHandler:
    def __init__(self):

        self.qa_chain = None

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=150,
        )

        logging.debug('Loading Embeddings')
        self.embeddings = HuggingFaceInstructEmbeddings(
            model_name='hkunlp/instructor-xl',
            model_kwargs={"device": "cpu"},
        )
        logging.debug('Loaded Embeddings')

        logging.debug('Loading Falcon LLM')
        self.falcon_llm = HuggingFaceHub(
            repo_id='tiiuae/falcon-7b-instruct',
            model_kwargs={"temperature": 0.1,
                          "max_new_tokens": 500, "use_cache": False},

        )
        logging.debug('Loaded Falcon LLM')

        template_string = """
        The transcribed text of an audio/video file is provided, enclosed within triple backticks.\
        Refer to this transcribed text to answer the following question. The answer must be clear and concise.\

        If you do not know the answer just say you don't know. Do not make up an answer.\
        If you did not understand the question, say that you did not understand the question.\
        
        Audio/Video Transcription: ```{context}```

        Question:{question}

        Answer:
        """

        self.prompt_template = PromptTemplate.from_template(template_string)
        self.memory = ConversationBufferWindowMemory(
            k=1, memory_key="chat_history", return_messages=True)

    def load_text(self, _docs, chain_type='stuff'):

        texts = self.text_splitter.split_documents(_docs)

        db = FAISS.from_documents(texts, self.embeddings)

        retriever = db.as_retriever(search_kwargs={"k": 3})

        self.memory.clear()

        self.qa_chain = RetrievalQA.from_llm(
            llm=self.falcon_llm,
            retriever=retriever,
            memory=self.memory,
            prompt=self.prompt_template,
            verbose=False,
        )

    def query(self, query, callbacks=[]):
        if not self.qa_chain:
            raise TypeError('Error Loading File')

        try:
            result = self.qa_chain.run(query)
            return result
        except ConnectionError:
            return ':red[Failed to Connect]'
        except ValueError as e:
            return f':red[{str(e)}]'
        except Exception as e:
            return f':red[{str(e)}]'
