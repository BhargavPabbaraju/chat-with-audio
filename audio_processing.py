from constants import FileType,Language
from math import ceil

import os


import logging

import speech_recognition as sr 
from pydub import AudioSegment


AudioSegment.ffmpeg = 'ffmpreg.exe'
AudioSegment.ffprobe = 'fforobe.exe'

#Speech Recognizer
recognizer = sr.Recognizer()


class AudioProcessor:
    def __init__(self):
        self.chunks = None
    
    def get_chunks(self,data,file_name,input_type=FileType.FILE):
        '''
        Split audio into chunks and convert audio from wav/ogg/mp3 into wav for google speech recognition api

        Args:
            data(streamlit.runtime.uploaded_file_manager.UploadedFile or bytes): The audio data from the uploaded file or recorded bytes
            file_name(str): The audio file path (is one of 'audio.wav','audio.mp3','audio.ogg')
            input_type(FileType,optional): Whether the audio is from a file or from the microphone. Deafaults to File Input.
        
        Returns:
            audios(list): List of chunks converted into wav format ready to be transcribed by Google Speech Recognition API
        
        '''
        logging.debug('Entered the get_chunks function')
        with open(file_name,"wb") as f:
            if input_type==FileType.RECORD:
                f.write(data)
            else:
                f.write(data.getbuffer())
        
        logging.info('Input Audio saved as '+file_name)

        try:
            audio = AudioSegment.from_file(file_name)
            chunk_duration = 60 * 1000 #one minute
            total_duration = len(audio)
            logging.info(f'Audio has a total duration of {total_duration/60000} minutes')
            logging.info(f'Audio split into {ceil(total_duration/chunk_duration)} chunks')
            
            
            #Create a folder to save audio chunks
            folder_name = "audio-chunks"
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)

            audios=[]

            chunk_number = 1
            for start_time in range(0,total_duration,chunk_duration):
                end_time = start_time + chunk_duration
                chunk = audio[start_time:end_time]
                file_name = os.path.join(folder_name,f'chunk{chunk_number}.wav')
                chunk.export(
                    file_name,
                    format='wav',
                    parameters=["-ac", "1", "-ar", "16000"]
                    )
                with sr.AudioFile(file_name) as source:
                    audios.append(recognizer.record(source))

                chunk_number+=1
                logging.info('Saved '+file_name)
            
            
            
            return audios

        except:
            logging.exception('Could not load input')
            raise ValueError('Could not load input')


  


    def transcribe_free(self,chunks,language=Language.USENGLISH):
        '''
        Returns the transcribed text from audio using Google Speech Recognition API

        Args:
            audios(list): List of chunks converted into wav format ready to be transcribed by Google Speech Recognition API
            language(Language,optional): The language the transcribed text should be in. Defaults to US English.
        
        Returns:
            text(str):  The transcribed text in the language requested.
        
        Raises:
            ValueError: If there is an error opening the file or if the Speech Recognizer cannot understand the audio.
            ConnectionError:    If the API call couldn't be made (Either no Internet or large file)

        '''

        
        
        for audio in chunks:
            try:
                text =recognizer.recognize_google(audio,language=language)
                yield text
            except sr.UnknownValueError:
                raise ValueError("Speech Recognizer could not understand the audio")
                
            except sr.RequestError as e:
                raise ConnectionError(f"Could not request results from Google Speech Recognition service; {e}")
        
    
       

    