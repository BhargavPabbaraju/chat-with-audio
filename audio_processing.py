

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
        audio = AudioSegment.from_file(audio_file)
        audio.export("audio.wav",format="wav", parameters=["-ac", "1", "-ar", "16000"])
        with sr.AudioFile("audio.wav") as source:
            audio = recognizer.record(source)

        return audio


    def transcribe_free(self,data,file_name,input_type='file'):
        with open(file_name,"wb") as f:
            if input_type=='record':
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
                
    
            