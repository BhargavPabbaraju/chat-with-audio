# Features Wanted

- Load Youtube Video from url
- Load Audio from file input , Supported types :(.wav,.mp3,.ogg)
- Both free and OpenAI API Key Systems:
- Summarize audio
- Ask questions about audio
- Supported Languages List:
- Support Huge audio files , State size limits
- Error handling and fallback to Free version

### Common Stuff:

- Use Langchain youtube loader to load youtube videos
- Use Google Text to Speech APi for text to speech

### With OpenAI API Key:

- Use Whisper to transcribe and translate audio
- Specify information/instructions to transcribe audio (Optional)
- Use gpt-turbo-3.5 to summarize and ask questions on the transcribed text

### Free version

- Use SpeechRecognition to transcribe and translate audio
- Use falcon -7b llm for summarizing and q/a

# Priorities

- Create Python venv - Done
- Streamlit app base - Done
- Audio input and saving - Done
- SpeechRecognition to transcribe and translate audio - Done
- Language Testing on 4 languages : Hindi , Telugu , English and Japanese - Done
- Basic Chat Interface - Done
- Integrate Falcon and summarize and q/a test - Done
- Loading circles/text - Done
- Breakdown audio into chunks - Done
- Youtube video loader and run above steps - Done
- Test multiple language youtube videos - Done
- Remove Ads from Youtube videos - Half Done
- Display Chunk number

- Whisper to transcribe audio
- Language Testing on 4 languages : Hindi , Telugu , English and Japanese
- gpt-turbo-3.5 to summarize and ask questions on the transcribed text

- Initial deployment

- Test audio file sizes
