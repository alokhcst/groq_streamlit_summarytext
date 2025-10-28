# Voice Summary Setup Guide

## Features
- **Direct Microphone Recording**: Record your voice directly in the browser using `st.audio_input()`
- **Automatic Transcription**: Speech is automatically converted to text using Google Speech Recognition
- **AI-Powered Summarization**: Transcribed text is sent to Groq LLM for a 4-point summary
- **Real-time Streaming**: Summary is streamed in real-time as it's generated

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg (Required for audio format conversion)**:
   
   **Windows:**
   - Download from https://ffmpeg.org/download.html
   - Extract and add to PATH, or install via chocolatey: `choco install ffmpeg`
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

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
- Speech recognition is powered by Google's Speech Recognition API (free, no API key required)
- You must grant microphone permissions to your browser for the recording feature to work
- Summarization uses Groq's fast inference LLM models
- You can choose from different Groq models for summarization

## Troubleshooting

- **No audio detected**: Make sure you grant microphone permissions to your browser
- **Transcription failed**: Check your internet connection (Google Speech Recognition requires internet)
- **Groq API error**: Verify your API key is correctly set in secrets.toml

