
from langchain.document_loaders.generic import GenericLoader
from typing import Iterable, Iterator, List

from langchain.document_loaders.base import BaseBlobParser
from langchain.document_loaders.blob_loaders import Blob, BlobLoader
from langchain.document_loaders.blob_loaders.schema import Blob
from langchain.schema import Document

from pydub import AudioSegment

import logging

import os

from math import ceil

import speech_recognition as sr

from datetime import timedelta

from utils.constants import Language


AudioSegment.ffmpeg = 'ffmpeg.exe'
AudioSegment.ffprobe = 'ffprobe.exe'
AudioSegment.converter = "ffmpeg.exe"


def format_time(millis):
    '''
    Formats time from milliseconds to HH:MM:SS

    Args:
        millis(int):   Time in milliseconds
    Returns:
        time(str):  Time formatted as HH:MM:SS

    '''
    return str(timedelta(seconds=millis/1000))


class SpeechRecognitionParser(BaseBlobParser):
    def __init__(self, language: Language = Language.US_ENGLISH) -> None:
        """
        Initializes speech recognition module

        Args:
            language: The transcribed text will be in this language.
        """
        self.recognizer = sr.Recognizer()
        self.language = language

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:

        try:
            audio = AudioSegment.from_file(blob.path)

            chunk_duration = 60 * 1000  # one minute
            total_duration = len(audio)
            total_chunks = ceil(total_duration/chunk_duration)
            logging.info(
                f'Audio has a total duration of {total_duration/60000} minutes')
            logging.info(f'Audio split into {total_chunks} chunks')

            # Create a folder to save audio chunks
            folder_name = "audio-chunks"
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)

            chunk_number = 1
            for start_time in range(0, total_duration, chunk_duration):
                end_time = start_time + chunk_duration
                chunk = audio[start_time:end_time]
                file_name = os.path.join(
                    folder_name, f'chunk{chunk_number}.wav')
                chunk.export(
                    file_name,
                    format='wav',
                    parameters=["-ac", "1", "-ar", "16000"]
                )

                metadata = {'start_time': start_time, 'end_time': end_time,
                            'source': blob.source, 'chunk': chunk_number}

                with sr.AudioFile(file_name) as source:
                    sound = self.recognizer.record(source)
                try:
                    text = self.recognizer.recognize_google(
                        sound, language=str(self.language.value))
                    yield Document(page_content=text, metadata=metadata)
                except sr.UnknownValueError:
                    logging.exception(
                        f"Speech Recognizer could not understand the audio from {format_time(start_time)} to {format_time(end_time)}")
                    yield Document(page_content='', metadata=metadata)
                    # raise ValueError("Speech Recognizer could not understand the audio")

                except sr.RequestError as e:
                    logging.exception(
                        f"Could not request results from Google Speech Recognition service;")
                    yield Document(page_content='', metadata=metadata)
                    # raise ConnectionError(f"Could not request results from Google Speech Recognition service; {e}")

                chunk_number += 1
                logging.info('Saved '+file_name)
        except:
            logging.exception('Could not load input')
            raise ValueError('Could not load input')


class AudioLoader(BlobLoader):
    def __init__(self, file_paths: List[str]) -> None:
        """
        Initialize AudioLoader with a list of file paths to load audio files from

        Args:
            file_paths: A list of file paths to load audio files from
        """
        self.file_paths = file_paths

    def yield_blobs(self) -> Iterable[Blob]:
        """
        Yield blobs from each file path provided
        """
        for path in self.file_paths:
            yield Blob.from_path(path)
