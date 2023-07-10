
import streamlit as st

from audio_processing import AudioProcessor


audio_processor = AudioProcessor()

class Transcriber:
    '''
        Transcribes speech to text , either using the GoogleSpeechRecognitionAPI or Whisper API
    '''
    def __init__(self,type='free'):
        self.type = type
        self.loading_text = st.empty()
    
    def loading(self,message):
        with self.loading_text.container():
            st.write(message)

    def clear_loading_message(self):
        self.loading_text.empty()

    
    def transcribe_free(self,data,file_name,input_type='file'):
        try:
            self.loading('Speech Processing In Progress...Please Wait...')
            text = audio_processor.transcribe_free(data,file_name,input_type)
            st.write('Transcribed Text:')
            st.write(f'**{text}**')
            
        except ValueError as e:
            st.write(e)
        except ConnectionError as e:
            st.write(e)
        finally:
            self.clear_loading_message()
