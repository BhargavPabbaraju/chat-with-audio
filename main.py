
import logging

from langchain.llms import OpenAI,HuggingFaceHub
from langchain import PromptTemplate
from langchain.chains import LLMChain,SequentialChain



import streamlit as st
from audio_recorder_streamlit import audio_recorder

from speech_tool import Transcriber

from constants import FileType


###Loading API Keys
import os
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]


#LLMS
repo_id = 'tiiuae/falcon-7b-instruct'
falcon_llm = HuggingFaceHub(
    repo_id=repo_id,
    model_kwargs={"temperature":0.1,"max_new_tokens":500},
    )



logging.basicConfig(
    filename='debug.log',
    filemode="w",
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    )


#streamlit framework 
st.title('Chat With Audio')



###Input Options
input_options = ['Load Audio File','Record Audio','Youtube URL']
input_container = st.container()

##Audio Tools
transcriber = Transcriber(st.container())

def change_option():
    global option
    option = st.session_state.input_option
    


with input_container.container():
    option = st.radio(
        label='Select an Option',
        options=input_options,
        key='input_option',
        on_change=change_option,
        horizontal=True
        )






#Upload Audio File
if  option == input_options[0]:
    with input_container.container():
        audio_file = st.file_uploader("Choose a file",type=['wav','mp3','ogg'])
        if audio_file:
            file_type = audio_file.type.split('/')[1]
            transcriber.transcribe_free(audio_file,'audio.'+file_type,input_type=FileType.FILE)

       
        
       

#Record Audio
elif option == input_options[1]:  
    with input_container.container():
        audio_bytes = audio_recorder(
            text="Click to Record",
            recording_color="#28B463",
            neutral_color="#E74C3C",
            icon_name="microphone",
            icon_size="3x",
            pause_threshold=300.0,

        )
        if audio_bytes:
            with input_container.container():
                st.audio(audio_bytes)
            transcriber.transcribe_free(audio_bytes,'audio.wav',input_type=FileType.RECORD)
        

    


#Youtube Url Input
else:
    with input_container.container():
        youtube_url = st.text_input("Enter Youtube url",key='youtube_url')

    
