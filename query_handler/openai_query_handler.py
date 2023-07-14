
import logging


from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings


from query_handler.abstract_query_handler import AbstractQueryHandler

from typing import Optional


class OpenAIQueryHandler(AbstractQueryHandler):
    def __init__(self, api_key: Optional[str] = None):
        self.openai_api_key = api_key
        super().__init__()

    def load_embeddings(self):
        logging.debug('Loading OpenAI Embeddings')
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        logging.debug('Loading OpenAI Embeddings')

    def load_llm(self):
        logging.debug('Loading GPT LLM')
        self.falcon_llm = ChatOpenAI(
            model_name='gpt-3.5-turbo',
            temperature=0,
            openai_api_key=self.openai_api_key
        )
        logging.debug('Loaded GPT LLM')
