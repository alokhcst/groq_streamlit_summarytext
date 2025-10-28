# Voice Summary Setup Guide

## Features
- **Direct Microphone Recording**: Record your voice directly in the browser using `st.audio_input()`
- **Automatic Transcription**: Speech is automatically converted to text using OpenAI Whisper (no FFmpeg required!)
- **AI-Powered Summarization**: Transcribed text is sent to Groq LLM for a 4-point summary
- **Real-time Streaming**: Summary is streamed in real-time as it's generated
- **Cloud-Ready**: Works on Streamlit Community Cloud without additional dependencies

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: For Streamlit Community Cloud deployment, FFmpeg is NOT required. The app uses OpenAI Whisper which handles audio conversion internally.

2. **Optional: Install FFmpeg (Only for local development with Google Speech Recognition)**:
   
   FFmpeg is NOT required for Streamlit Community Cloud. The app uses OpenAI Whisper which works without FFmpeg.
   
   If you want to use Google Speech Recognition locally, install FFmpeg:
   - **Windows**: Download from https://ffmpeg.org/download.html or run `choco install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

3. **Set up your Groq API Key** in `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY="your_api_key_here"
   ```

4. **Run the App**:
   ```bash
   streamlit run streamlit_app.py
   ```

## How to Use

1. **Record Your Voice**:
   - Click the microphone button in the browser
   - Grant microphone permissions when prompted
   - Speak your thoughts/message
   - Stop recording when done

2. **Automatic Processing**:
   - Your speech is automatically transcribed
   - The transcription is displayed
   - Groq LLM generates a 4-point summary
   - The summary streams in real-time

3. **View History**:
   - All transcriptions and summaries are saved in chat history
   - Use the "Clear Chat History" button to reset

## Notes

- The app uses Streamlit's built-in `st.audio_input()` for direct browser microphone recording
- Speech recognition uses OpenAI Whisper (free, local processing, no API key required)
- Fallback to Google Speech Recognition if Whisper is not installed
- FFmpeg is NOT required for most deployments (including Streamlit Community Cloud)
- You must grant microphone permissions to your browser for the recording feature to work
- Summarization uses Groq's fast inference LLM models
- You can choose from different Groq models for summarization

## Troubleshooting

- **No audio detected**: Make sure you grant microphone permissions to your browser
- **Transcription failed**: 
  - First run will download Whisper model (~140 MB) - this is normal
  - For Google Speech Recognition fallback: Check your internet connection
  - Make sure audio is clear and loud enough
- **Groq API error**: Verify your API key is correctly set in secrets.toml
- **FFmpeg error on cloud**: You're using the old version - update to latest code that uses Whisper

