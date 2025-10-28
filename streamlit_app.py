import streamlit as st
from typing import Generator
from groq import Groq
import tempfile
import os
import io
import sys

# Handle aifc import issue for SpeechRecognition (required in some Python versions)
try:
    import aifc
except ImportError:
    # Add a minimal stub module to sys.modules
    import types
    aifc_module = types.ModuleType('aifc')
    sys.modules['aifc'] = aifc_module

# Now import speech_recognition
import speech_recognition as sr

st.set_page_config(page_icon="🎤", layout="wide",
                   page_title="Voice Summary with Groq!")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("🎤")

st.subheader("Voice Summary Assistant with Groq", divider="rainbow", anchor=False)

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

# Define model details
models = {
    "llama-3.1-8b-instant": {"name": "LLaMA3.1-8b-instant", "tokens": 128000, "developer": "Meta"},
    "groq/compound": {"name": "groq/compound", "tokens": 8192, "developer": "Groq"},
    "llama-3.3-70b-versatile": {"name": "LLaMA3.3-70b-versatile", "tokens": 128000, "developer": "Meta"},
    "groq/compound-mini": {"name": "groq/compound-mini", "tokens": 8192, "developer": "Groq"},
}

# Layout for controls
col1, col2 = st.columns(2)

with col1:
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=0
    )

max_tokens_range = models[model_option]["tokens"]

with col2:
    max_tokens = st.slider(
        "Max Tokens:",
        min_value=512,
        max_value=min(32768, max_tokens_range),
        value=min(4096, max_tokens_range),
        step=512,
    )


def transcribe_audio(audio_bytes, file_extension='webm'):
    """Transcribe audio bytes to text using Google Speech Recognition."""
    tmp_file_path = None
    wav_path = None
    
    try:
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        # Convert to WAV if needed using pydub
        wav_path = tmp_file_path
        if file_extension != 'wav':
            try:
                from pydub import AudioSegment
                
                # Load audio and convert to WAV
                audio = AudioSegment.from_file(tmp_file_path)
                wav_path = tmp_file_path.replace(f".{file_extension}", ".wav")
                audio.export(wav_path, format="wav")
                
                # Clean up original file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
            except ImportError:
                return "Error: pydub is not installed. Please run: pip install pydub"
            except Exception as conv_error:
                return f"Error during audio conversion: {str(conv_error)}\nTip: Make sure FFmpeg is installed."
        
        # Use SpeechRecognition to transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)
        
        # Transcribe using Google Speech Recognition
        text = recognizer.recognize_google(audio_data)
        
        return text
        
    except sr.UnknownValueError:
        return "Could not understand audio - audio might be too quiet or unclear"
    except sr.RequestError as e:
        return f"Speech recognition service error: {str(e)}"
    except FileNotFoundError as e:
        return f"Audio file not found: {str(e)}"
    except Exception as e:
        return f"Unexpected error during transcription: {str(e)}"
    finally:
        # Clean up temporary files
        try:
            if wav_path and os.path.exists(wav_path):
                os.unlink(wav_path)
            if tmp_file_path and tmp_file_path != wav_path and os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
        except:
            pass


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def get_summary_prompt(transcribed_text):
    """Create a prompt for Groq to summarize in 4 points."""
    prompt = f"""Please summarize the following text in exactly 4 key points:
    
{transcribed_text}

Provide the summary as 4 numbered points."""
    return prompt


# Display transcribed text section
if st.session_state.transcribed_text:
    st.markdown("### 📝 Transcribed Text")
    st.text_area("Your speech:", st.session_state.transcribed_text, disabled=True, height=150)

# Main audio recording interface
st.markdown("### 🎤 Record Your Voice")

# Audio input for microphone recording
audio_input = st.audio_input(
    "Click to record your voice for summary",
    key="audio_input"
)
file_extension = 'webm'  # audio_input returns webm format (opus codec)

if audio_input:
    st.success("✅ Audio recorded! Processing...")
    
    # Get audio bytes - handle both UploadedFile and bytes
    try:
        if hasattr(audio_input, 'read'):
            audio_bytes = audio_input.read()
        else:
            audio_bytes = audio_input
    except Exception as e:
        st.error(f"Error reading audio: {e}", icon="🚨")
        audio_bytes = None
    
    if audio_bytes:
        # Transcribe the audio
        transcribed_text = transcribe_audio(audio_bytes, file_extension)
        
        # Process successful transcription
        if transcribed_text and "Could not understand" not in transcribed_text and "Error" not in transcribed_text:
            st.session_state.transcribed_text = transcribed_text
            
            # Create summary prompt
            summary_prompt = get_summary_prompt(transcribed_text)
            
            # Add user message to chat
            st.session_state.messages.append({
                "role": "user",
                "content": f"Audio transcription: {transcribed_text}"
            })
            
            # Display transcription in chat
            with st.chat_message("user", avatar='👤'):
                st.markdown(f"**Transcribed:** {transcribed_text}")
            
            # Fetch response from Groq API for summary
            try:
                messages = [
                    {
                        "role": "user",
                        "content": summary_prompt
                    }
                ]
                
                chat_completion = client.chat.completions.create(
                    model=model_option,
                    messages=messages,
                    max_tokens=max_tokens,
                    stream=True
                )
                
                # Stream the summary response
                with st.chat_message("assistant", avatar="🤖"):
                    chat_responses_generator = generate_chat_responses(chat_completion)
                    full_response = st.write_stream(chat_responses_generator)
                    
                    # Add summary to messages
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response
                    })
                    
            except Exception as e:
                st.error(f"Error generating summary: {e}", icon="🚨")
        else:
            st.error("❌ Transcription failed", icon="🚨")
            st.error(f"Error details: {transcribed_text}")
            
            # Show helpful installation tips
            with st.expander("🔧 Troubleshooting Tips"):
                st.markdown("""
                ### Common Issues and Solutions:
                
                1. **FFmpeg not installed** (most common issue):
                   - Windows: Download from https://ffmpeg.org/download.html or run `choco install ffmpeg`
                   - Add FFmpeg to your system PATH
                   - Restart your terminal after installation
                
                2. **pydub not installed**:
                   ```bash
                   pip install pydub
                   ```
                
                3. **Audio too quiet or unclear**:
                   - Speak clearly and loudly
                   - Record in a quiet environment
                   - Check your microphone settings
                
                4. **Check your internet connection**:
                   - Google Speech Recognition requires internet access
                """)
    else:
        st.error("Error: Could not read audio bytes")

# Display chat history
st.markdown("### 💬 Chat History")
if st.session_state.messages:
    for message in st.session_state.messages:
        avatar = '🤖' if message["role"] == "assistant" else '👤'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Clear history button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.transcribed_text = ""
        st.rerun()
