import logging

from typing import Optional, List
from langchain.schema import Document

from utils.constants import FileType, Language

from yt_dlp.utils import DownloadError

import streamlit as st

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.blob_loaders import YoutubeAudioLoader


from speech_tools.audio_processing import format_time, AudioLoader, SpeechRecognitionParser


def get_generator(_loader, language):
    loader = GenericLoader(_loader, SpeechRecognitionParser(language=language))
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
        self.data = None

    def set_container(self, container):

        self.container = container

    def get_docs(self):
        return self.docs

    def get_text(self):
        return '\n'.join([x.page_content for x in self.docs])

    def transcribe_free(self, data, file_path: str, input_type, language: Language = Optional[Language.US_ENGLISH]) -> List[Document]:
        '''
        Displays the Transcribed text using GoogleSpeechRecognitionAPI , results may be inaccurate.

        Args:
            file_path: The audio file path 
            input_type: Whether the audio is from a file or from the microphone. Deafaults to File Input.
            language: The language the transcribed text should be in. Defaults to US English.
        Returns:
            docs: List of transcribed documents as langchain Documents
        '''

        logging.debug(f"Transcribe free method is called with File Path:{file_path} , Input Type:{input_type} and\
                      Language:{str(language.value)}")

        # If same audio data is passed , just return already computed documents
        if data == self.data:
            self.container.markdown(f':green[**{self.get_text()}**]')
            return self.docs
        else:
            self.data = data

        self.got_input = False
        self.processing = False

        self.loading_text = self.container.empty()

        if input_type != FileType.YOUTUBE:
            with open(file_path, 'wb') as f:
                f.write(data)

            loader = AudioLoader(file_paths=[file_path])

        else:
            loader = YoutubeAudioLoader([data], save_dir=file_path)

        try:
            with self.loading_text.container():
                st.markdown(
                    f':blue[Speech Processing In Progress...Please Wait...]')

            self.got_input = True
            self.processing = True

            self.container.markdown(f':blue[Transcribed Text:]')
            text_generator = get_generator(loader, language)

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
                    self.docs.append(result)
                else:
                    logging.debug(f'Could not transcribe Text of {chunk}')
                    self.container.markdown(
                        f':red[**Could not transcribe audio from {chunk}**]')

            return self.docs

        except ValueError as e:
            self.container.markdown(f':red[{e}]')
        except ConnectionError as e:
            self.container.markdown(f':red[{e}]')
        except DownloadError as e:
            self.container.markdown(f':red[Invalid Youtube URL]')
        finally:
            self.loading_text.empty()
            self.processing = False
