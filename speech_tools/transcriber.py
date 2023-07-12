import logging

from typing import Optional, List
from langchain.schema import Document

from utils.constants import FileType, Language

import streamlit as st

from langchain.document_loaders.generic import GenericLoader


from speech_tools.audio_processing import format_time, AudioLoader, SpeechRecognitionParser


@st.cache_resource(
    hash_funcs={st.delta_generator.DeltaGenerator: lambda x: None},
    show_spinner=False
)
def get_generator(file_path, language):
    loader = GenericLoader(AudioLoader(
        file_paths=[file_path]), SpeechRecognitionParser(language=language))
    text_generator = loader.lazy_load()
    return text_generator


class Transcriber:
    '''
        Transcribes speech to text , either using the GoogleSpeechRecognitionAPI or Whisper API
    '''

    def __init__(self, type='free'):
        self.type = type
        self.got_input = False
        self.processing = False
        self.docs = []

    def set_container(self, container):

        self.container = container

    def get_docs(self):
        return self.docs

    def get_text(self):
        return '\n'.join([x.page_content for x in self.docs])

    def refresh_docs(self):
        self.docs = []

    def transcribe_free(self, file_path: str, language: Language = Optional[Language.US_ENGLISH]) -> List[Document]:
        '''
        Displays the Transcribed text using GoogleSpeechRecognitionAPI , results may be inaccurate.

        Args:
            file_path: The audio file path 
            input_type: Whether the audio is from a file or from the microphone. Deafaults to File Input.
            language: The language the transcribed text should be in. Defaults to US English.
        Returns:
            docs: List of transcribed documents as langchain Documents
        '''

        if len(self.docs) > 0:
            full_text = '\n'.join([x.page_content for x in self.docs])
            self.container.markdown(f':green[**{full_text}**]')
            return self.docs

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
            text_generator = get_generator(file_path, language)

            self.docs = []
            for result in text_generator:
                self.loading_text.empty()
                with self.loading_text.container():
                    chunk = format_time(
                        result.metadata["start_time"]) + ' to ' + format_time(result.metadata["end_time"])
                    st.markdown(f':orange[Processing {chunk}]')

                text = result.page_content
                if text:
                    self.container.markdown(f':green[**{text}**]')
                    logging.debug(f'Transcribed Text of {chunk} : {text}')
                else:
                    logging.debug(f'Could not transcribe Text of {chunk}')
                    self.container.markdown(
                        f':red[**Could not transcribe audio from {chunk}**]')

                self.docs.append(result)

            return self.docs

        except ValueError as e:
            self.container.markdown(f':red[{e}]')
        except ConnectionError as e:
            self.container.markdown(f':red[{e}]')
        finally:
            self.loading_text.empty()
            self.processing = False
