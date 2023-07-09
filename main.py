
###Loading API Keys
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]


from langchain.llms import OpenAI,HuggingFaceHub
from langchain import PromptTemplate
from langchain.chains import LLMChain,SequentialChain

import streamlit as st
from audio_recorder_streamlit import audio_recorder

import speech_recognition as sr 
from pydub import AudioSegment
AudioSegment.ffmpeg = 'ffmpreg.exe'
AudioSegment.ffprobe = 'fforobe.exe'




#LLMS
repo_id = 'tiiuae/falcon-7b-instruct'
falcon_llm = HuggingFaceHub(repo_id=repo_id,model_kwargs={"temperature":0.1,"max_new_tokens":500})

#Speech Recognizer
recognizer = sr.Recognizer()

#streamlit framework 
st.title('Chat With Audio')


###Input Options

input_options = ['Load Audio File','Record Audio','Youtube URL']


def change_option():
    global option
    option = st.session_state.input_option
    


option = st.radio(
    label='Select an Option',
    options=input_options,
    key='input_option',
    on_change=change_option,
    horizontal=True
    )

def convert_audio(audio_file):

    audio = AudioSegment.from_file(audio_file)
    audio.export("audio.wav",format="wav", parameters=["-ac", "1", "-ar", "16000"])
    with sr.AudioFile("audio.wav") as source:
        audio = recognizer.record(source)
    
    return audio



def transcribe_free(data,file_name,input_type='file'):
    with open(file_name,"wb") as f:
        if input_type=='record':
            f.write(data)
        else:
            f.write(data.getbuffer())
    

    try:
        audio = convert_audio(file_name)
    except:
        audio = None
        st.write('Error opening input')

    if audio:
        try:
            st.write('Converting Speech to Text....')
            text = recognizer.recognize_google(audio)
            st.write("Transcribed Text:")
            st.write(f'**{text}**')
            st.write('Successfully Converted....')
        except sr.UnknownValueError:
            st.write("Speech Recognizer could not understand the audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
   
        


#Upload Audio File
if  option == input_options[0]:
    audio_file = st.file_uploader("Choose a file",type=['wav','mp3','ogg'])
    if audio_file:
        file_type = audio_file.type.split('/')[1]
        transcribe_free(audio_file,'audio.'+file_type,input_type='file')
       
        
       

#Record Audio
elif option == input_options[1]:  
    audio_bytes = audio_recorder(
        text="Click to Record",
        recording_color="#28B463",
        neutral_color="#E74C3C",
        icon_name="microphone",
        icon_size="3x",
        pause_threshold=300.0,

    )
    if audio_bytes:
        st.audio(audio_bytes)
        transcribe_free(audio_bytes,'audio.wav',input_type='record')

    


#Youtube Url Input
else:
    youtube_url = st.text_input("Enter Youtube url",key='youtube_url')