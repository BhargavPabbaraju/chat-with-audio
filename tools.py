
import streamlit as st

from audio_processing import AudioProcessor


audio_processor = AudioProcessor()

class Transcriber:
    '''
        Transcribes speech to text , either using the GoogleSpeechRecognitionAPI or Whisper API
    '''
    def __init__(self,type='free'):
        self.type = type
        
    
    def transcribe_free(self,data,file_name,input_type='file'):
        self.loading_text = st.empty()
        try:
            with self.loading_text.container():
                st.markdown(f':blue[Speech Processing In Progress...Please Wait...]')
            text = audio_processor.transcribe_free(data,file_name,input_type)
            st.markdown(f':blue[Transcribed Text:]')
            st.markdown(f':green[**{text}**]')
            
        except ValueError as e:
            st.markdown(f':red[{e}]')
        except ConnectionError as e:
            st.markdown(f':red[{e}]')
        finally:
            self.loading_text.empty()
