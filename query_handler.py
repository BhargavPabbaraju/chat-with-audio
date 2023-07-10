
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain import HuggingFaceHub
from langchain.embeddings import HuggingFaceInstructEmbeddings

import logging

###Loading API Keys
import os
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]




class LLMQueryHandler:
    def __init__(self):

        self.qa_chain = None
        self.text_splitter = RecursiveCharacterTextSplitter(
                                chunk_size = 1000,
                                chunk_overlap = 200,
                            )

        logging.debug('Loading Embeddings')
        self.embeddings = HuggingFaceInstructEmbeddings(
                                    model_name='hkunlp/instructor-xl',
                                    model_kwargs={"device":"cpu"},
                                )
        logging.debug('Loaded Embeddings')

        logging.debug('Loading Falcon LLM')
        self.falcon_llm = HuggingFaceHub(
                            repo_id = 'tiiuae/falcon-7b-instruct',
                            model_kwargs={"temperature": 0.1, "max_new_tokens": 500}
                )
        logging.debug('Loaded Falcon LLM')

    def load_text(self,text,chain_type='stuff'):
        with open('text.txt','w') as f:
            f.write(text)
        
        loader = TextLoader('text.txt')
        docs = loader.load()

        texts = self.text_splitter.split_documents(docs)

        db = FAISS.from_documents(texts,self.embeddings)

        retriever = db.as_retriever(search_kwargs={"k":3})

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.falcon_llm,
            chain_type=chain_type,
            retriever=retriever,
            return_source_documents=True,
            )

    
    def query(self,query):
        if not self.qa_chain:
            raise TypeError('Error Loading File')
        
        try:
            return self.qa_chain(query)['result']
        except ConnectionError:
            return ':red[Failed to Connect]'
            
        

