from constants import FileType,Language

import speech_recognition as sr 
from pydub import AudioSegment
from pydub.silence import split_on_silence
AudioSegment.ffmpeg = 'ffmpreg.exe'
AudioSegment.ffprobe = 'fforobe.exe'

#Speech Recognizer
recognizer = sr.Recognizer()


class AudioProcessor:
    def __init__(self):
        pass
    
    def convert_audio(self,audio_file):
        '''
        convert audio from wav/ogg/mp3 into wav for google speech recognition api

        Args:
            audio_file(str): The audio file path (is one of 'audio.wav','audio.mp3','audio.ogg')
        
        Returns:
            audio(speech_recognition.audio.AudioData): The audio converted into wav format ready to be transcribed by Google Speech Recognition API
        
        '''
        audio = AudioSegment.from_file(audio_file)
        audio.export("audio.wav",format="wav", parameters=["-ac", "1", "-ar", "16000"])
        with sr.AudioFile("audio.wav") as source:
            audio = recognizer.record(source)

        
        return audio


    def transcribe_free(self,data,file_name,input_type=FileType.FILE,language=Language.USENGLISH):
        '''
        Returns the transcribed text from audio using Google Speech Recognition API

        Args:
            data(streamlit.runtime.uploaded_file_manager.UploadedFile or bytes): The audio data from the uploaded file or recorded bytes
            file_name(str): The audio file path (is one of 'audio.wav','audio.mp3','audio.ogg')
            input_type(FileType,optional): Whether the audio is from a file or from the microphone. Deafaults to File Input.
            language(Language,optional): The language the transcribed text should be in. Defaults to US English.
        
        Returns:
            text(str):  The transcribed text in the language requested.
        
        Raises:
            ValueError: If there is an error opening the file or if the Speech Recognizer cannot understand the audio.
            ConnectionError:    If the API call couldn't be made (Either no Internet or large file)

        '''

        print(type(data))
        with open(file_name,"wb") as f:
            if input_type==FileType.RECORD:
                f.write(data)
            else:
                f.write(data.getbuffer())
        

        try:
            audio = self.convert_audio(file_name)
        except:
            audio = None
            raise ValueError('Error opening input')
            

        if audio:
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                raise ValueError("Speech Recognizer could not understand the audio")
                
            except sr.RequestError as e:
                raise ConnectionError(f"Could not request results from Google Speech Recognition service; {e}")
                
    
            