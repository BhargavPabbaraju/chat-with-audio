from constants import FileType,Language

import streamlit as st

from audio_processing import AudioProcessor

audio_processor = AudioProcessor()

class Transcriber:
    '''
        Transcribes speech to text , either using the GoogleSpeechRecognitionAPI or Whisper API
    '''
    def __init__(self,type='free'):
        self.type = type
        
    
    def transcribe_free(self,data,file_name,input_type=FileType.FILE,language=Language.USENGLISH):
        '''
        Displays the Transcribed text using GoogleSpeechRecognitionAPI , results may be inaccurate.

        Args:
            data(streamlit.runtime.uploaded_file_manager.UploadedFile or bytes): The audio data from the uploaded file or recorded bytes
            file_name(str): The audio file path (is one of 'audio.wav','audio.mp3','audio.ogg')
            input_type(FileType,optional): Whether the audio is from a file or from the microphone. Deafaults to File Input.
            language(Language,optional): The language the transcribed text should be in. Defaults to US English.
        '''
        self.loading_text = st.empty()
        try:
            with self.loading_text.container():
                st.markdown(f':blue[Speech Processing In Progress...Please Wait...]')
            
            audio = audio_processor.convert_audio(data,file_name,input_type)
            text_generator = audio_processor.transcribe_free(audio,language)
            
            st.markdown(f':blue[Transcribed Text:]')
            for text in text_generator:
                st.markdown(f':green[**{text}**]')
            
        except ValueError as e:
            st.markdown(f':red[{e}]')
        except ConnectionError as e:
            st.markdown(f':red[{e}]')
        finally:
            self.loading_text.empty()
