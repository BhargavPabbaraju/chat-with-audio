# Chat with Audio

Chat with Audio is an application that allows you to ask questions on audio files. It supports three types of user input:

1. **File Upload**: You can upload audio files in formats such as `.wav`, `.mp3`, and `.ogg`.
2. **Record Audio**: Record audio directly within the application.
3. **Download Audio from YouTube URL**: Provide a YouTube URL, and the application will download the audio from the video.

## Pricing Options

There are two versions available:

1. **OpenAI Version**: This version requires an OpenAI API Key. It utilizes OpenAI Embeddings and the GPT-3.5-turbo model for fast and high-quality results. Please refer to [OpenAI's pricing](https://openai.com/pricing) for details on associated costs.

2. **Free Version**: The free version uses HuggingFace Embeddings and Falcon LLM. Although it provides results at no cost, it is slower and may offer lower quality results. Please note that the free version may take up to 3 minutes to load embeddings.

## Transcription

The audio files are transcribed into text using the Google Speech Recognition API. The transcription process occurs minute by minute, complying with the free version of the API, allowing you to upload longer audio files.

## Supported Languages

Currently, the application supports transcription and question-answering in 22 languages.

Note: The purpose of this project is to facilitate asking questions on audio data using Large Language Models (LLMs).
