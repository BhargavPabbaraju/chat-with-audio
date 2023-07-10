from constants import FileType,Language

import streamlit as st

from audio_processing import AudioProcessor,format_time

audio_processor = AudioProcessor()





class Transcriber:
    '''
        Transcribes speech to text , either using the GoogleSpeechRecognitionAPI or Whisper API
    '''
    def __init__(self,container,type='free'):
        self.type = type
        self.container = container
        
    
    def transcribe_free(self,data,file_name,input_type=FileType.FILE,language=Language.USENGLISH):
        '''
        Displays the Transcribed text using GoogleSpeechRecognitionAPI , results may be inaccurate.

        Args:
            data(streamlit.runtime.uploaded_file_manager.UploadedFile or bytes): The audio data from the uploaded file or recorded bytes
            file_name(str): The audio file path (is one of 'audio.wav','audio.mp3','audio.ogg')
            input_type(FileType,optional): Whether the audio is from a file or from the microphone. Deafaults to File Input.
            language(Language,optional): The language the transcribed text should be in. Defaults to US English.
        '''
        self.loading_text = self.container.empty()
        full_text = ""
        try:
            with self.loading_text.container():
                st.markdown(f':blue[Speech Processing In Progress...Please Wait...]')
                    
            
            audio = audio_processor.convert_audio(data,file_name,input_type)
            text_generator = audio_processor.transcribe_free(audio,language)
            self.container.markdown(f':blue[Transcribed Text:]')
            for result in text_generator:
                self.loading_text.empty()
                with self.loading_text.container():
                    chunk = format_time(result["start_time"]) + ' to ' + format_time(result["end_time"])
                    st.markdown(f':blue[Processing {chunk}]')

                text = result['text']
                if text:
                    self.container.markdown(f':green[**{text}**]')
                    full_text+=text
                else:
                    self.container.markdown(f':red[**Could not transcribe audio from {chunk}**]')
            
        except ValueError as e:
            self.container.markdown(f':red[{e}]')
        except ConnectionError as e:
            self.container.markdown(f':red[{e}]')
        finally:
            self.loading_text.empty()
