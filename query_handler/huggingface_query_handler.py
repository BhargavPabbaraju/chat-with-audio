

from langchain import HuggingFaceHub
from langchain.embeddings import HuggingFaceInstructEmbeddings


import torch

import logging

from query_handler.abstract_query_handler import AbstractQueryHandler

# Loading API Keys


import streamlit as st

HUGGINGFACEHUB_API_TOKEN = st.secrets["HUGGINGFACEHUB_API_TOKEN"]


# Check if GPU is available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class HuggingFaceQueryHandler(AbstractQueryHandler):
    def load_embeddings(self):
        logging.debug('Loading HuggingFace Instruct Embeddings')
        self.embeddings = HuggingFaceInstructEmbeddings(
            model_name='hkunlp/instructor-xl',
            model_kwargs={"device": DEVICE},
        )
        logging.debug('Loading HuggingFace Instruct Embeddings')

    def load_llm(self):
        logging.debug('Loading Falcon LLM')
        self.falcon_llm = HuggingFaceHub(
            repo_id='tiiuae/falcon-7b-instruct',
            model_kwargs={"temperature": 0.1,
                          "max_new_tokens": 500, "use_cache": False},

        )
        logging.debug('Loaded Falcon LLM')
