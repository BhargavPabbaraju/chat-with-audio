import logging

from utils.constants import FileType, Language

import streamlit as st

from speech_tools.audio_processor import AudioProcessor, format_time


audio_processor = AudioProcessor()


@st.cache_resource(
    hash_funcs={st.delta_generator.DeltaGenerator: lambda x: None},
    show_spinner=False
)
def get_generator(data, file_name, input_type, language):
    audio = audio_processor.convert_audio(data, file_name, input_type)
    text_generator = audio_processor.transcribe_free(audio, language)
    return text_generator


class Transcriber:
    '''
        Transcribes speech to text , either using the GoogleSpeechRecognitionAPI or Whisper API
    '''

    def __init__(self, type='free'):
        self.type = type
        self.got_input = False
        self.processing = False
        self.data = None
        self.full_text = ""

    def set_container(self, container):

        self.container = container

    def get_text(self):
        return self.full_text

    def transcribe_free(self, data, file_name, input_type=FileType.FILE, language=Language.US_ENGLISH):
        '''
        Displays the Transcribed text using GoogleSpeechRecognitionAPI , results may be inaccurate.

        Args:
            data(streamlit.runtime.uploaded_file_manager.UploadedFile or bytes): The audio data from the uploaded file or recorded bytes
            file_name(str): The audio file path (is one of 'audio.wav','audio.mp3','audio.ogg')
            input_type(FileType,optional): Whether the audio is from a file or from the microphone. Deafaults to File Input.
            language(Language,optional): The language the transcribed text should be in. Defaults to US English.
        '''

        if self.data == data:
            return self.full_text
        else:
            self.data = data
            self.full_text = ""

        self.got_input = False
        self.processing = False

        self.loading_text = self.container.empty()

        try:
            with self.loading_text.container():
                st.markdown(
                    f':blue[Speech Processing In Progress...Please Wait...]')

            self.got_input = True
            self.processing = True

            self.container.markdown(f':blue[Transcribed Text:]')
            text_generator = get_generator(
                data, file_name, input_type, language)

            for result in text_generator:
                self.loading_text.empty()
                with self.loading_text.container():
                    chunk = format_time(
                        result["start_time"]) + ' to ' + format_time(result["end_time"])
                    st.markdown(f':blue[Processing {chunk}]')

                text = result['text']
                if text:
                    self.container.markdown(f':green[**{text}**]')
                    self.full_text += text
                    logging.debug(f'Transcribed Text of {chunk} : {text}')
                else:
                    logging.debug(f'Could not transcribe Text of {chunk}')
                    self.container.markdown(
                        f':red[**Could not transcribe audio from {chunk}**]')

            return self.full_text

        except ValueError as e:
            self.container.markdown(f':red[{e}]')
        except ConnectionError as e:
            self.container.markdown(f':red[{e}]')
        finally:
            self.loading_text.empty()
            self.processing = False
