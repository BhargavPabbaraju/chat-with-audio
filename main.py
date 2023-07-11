
import logging



import streamlit as st
from audio_recorder_streamlit import audio_recorder

from speech_tools import Transcriber
from query_handler import LLMQueryHandler

from constants import FileType



logging.basicConfig(
    filename='debug.log',
    filemode="w",
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    )

@st.cache_resource(show_spinner="Loading embeddings..May take several minutes...")
def query_handler_object():
    return LLMQueryHandler()

@st.cache_resource(show_spinner=False)
def transcriber_object():
    return Transcriber()

query_handler = query_handler_object()






#streamlit framework 
st.title('Chat With Audio')
input_container = st.container()
transcribe_col,chat_col = st.columns(2)




##Audio Tools
transcriber = transcriber_object() 
transcriber.set_container(transcribe_col)

###Input Options
input_options = ['Load Audio File','Record Audio','Youtube URL']





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
    


@st.cache_resource(show_spinner=False)
def load_text(text):
    #st.session_state.messages = []
    if len(text)==0:
        raise ValueError("Transcribed Text is Empty")
    query_handler.load_text(text)
        

#Upload Audio File
if  option == input_options[0]:
    with input_container.container():
        audio_file = st.file_uploader("Choose a file",type=['wav','mp3','ogg'])
        if audio_file:
            file_type = audio_file.type.split('/')[1]
            with transcribe_col:
                with st.spinner('Transcribing Audio...'):
                    transcriber.transcribe_free(
                                                audio_file,
                                                'audio.'+file_type,
                                                input_type=FileType.FILE
                                                )
            

       
        
       

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
            
            with transcribe_col:
                with st.spinner('Transcribing Audio...'):
                    transcriber.transcribe_free(
                                                audio_bytes,
                                                'audio.wav',
                                                input_type=FileType.RECORD
                                                )
        

    


#Youtube Url Input
else:
    with input_container.container():
        youtube_url = st.text_input("Enter Youtube url",key='youtube_url')


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
with chat_col:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



    
if transcriber.got_input and not transcriber.processing:
    process_prompt = False
    with chat_col:
        with st.spinner('Connting To LLM'):
            text = transcriber.get_text()
            logging.debug('Transcribed Text is'+text)
            try:
                load_text(text)
                process_prompt = True
            except ValueError as e:
                chat_col.markdown(f":red[{e}]")

    if process_prompt and (prompt:= st.chat_input("Say something")):
            with chat_col.chat_message("user"):
                st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
            
            try:
                reply = query_handler.query(prompt)
            except ConnectionError:
                reply = ':red[Failed to Connect]'
            with chat_col.chat_message("bot"):
                st.markdown(reply)
                st.session_state.messages.append({"role": "bot", "content": reply})



