
import logging


from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings


from query_handler.abstract_query_handler import AbstractQueryHandler


class OpenAIQueryHandler(AbstractQueryHandler):
    def load_embeddings(self):
        logging.debug('Loading OpenAI Embeddings')
        self.embeddings = OpenAIEmbeddings()
        logging.debug('Loading OpenAI Embeddings')

    def load_llm(self):
        logging.debug('Loading GPT LLM')
        self.falcon_llm = ChatOpenAI(
            model_name='gpt-3.5-turbo',
            temperature=0
        )
        logging.debug('Loaded GPT LLM')
