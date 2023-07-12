
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
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
            chunk_size=1000,
            chunk_overlap=200,
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
        The transcribed text of an audio file is provided, enclosed withinin triple backticks.\
        Refer to this transcribed text to answer the following questions.\
        
        If you do not know the answer just say you don't know. Do not make up an answer.\
        If you did not understand the question, say that you did not understand the question.\

        Audio Transcription: ```{context}```

        Question:{question}
        """

        self.prompt_template = PromptTemplate.from_template(template_string)
        self.memory = ConversationBufferWindowMemory(
            k=1, memory_key="chat_history", return_messages=True)
        # self.memory.save_context({"input":template_string},{"output":"Sure , give me a question"})

    def load_text(self, text, chain_type='stuff'):

        with open('outputs/text.txt', 'w') as f:
            f.write(text)

        loader = TextLoader('outputs/text.txt')
        docs = loader.load()

        texts = self.text_splitter.split_documents(docs)

        db = FAISS.from_documents(texts, self.embeddings)

        retriever = db.as_retriever(search_kwargs={"k": 3})

        self.memory.clear()

        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.falcon_llm,
            retriever=retriever,
            return_source_documents=False,
            memory=self.memory,
            chain_type=chain_type,
            verbose=True,
            combine_docs_chain_kwargs={"prompt": self.prompt_template}
        )

    def query(self, query):
        if not self.qa_chain:
            raise TypeError('Error Loading File')

        try:
            result = self.qa_chain({"question": query})
            return result['answer']
        except ConnectionError:
            return ':red[Failed to Connect]'
