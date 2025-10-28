import streamlit as st
from typing import Generator
from groq import Groq
import tempfile
import os

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
    """Transcribe audio bytes to text using OpenAI Whisper (NO FFmpeg required)."""
    tmp_file_path = None
    
    try:
        # Check if Whisper is installed
        try:
            import whisper
        except ImportError:
            return "Error: OpenAI Whisper is not installed. Please run: pip install openai-whisper"
        
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        # Load Whisper model (base model is good balance of speed and accuracy)
        with st.spinner("Loading Whisper model... (first time only)"):
            model = whisper.load_model("base")
        
        # Transcribe the audio
        with st.spinner("Transcribing audio..."):
            result = model.transcribe(tmp_file_path)
            text = result["text"]
        
        return text
        
    except Exception as e:
        return f"Error during transcription: {str(e)}"
    finally:
        # Clean up temporary file
        try:
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
        except:
            pass


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def get_summary_from_text(text):
    """Get summary from text input using Groq."""
    # Create summary prompt
    summary_prompt = get_summary_prompt(text)
    
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": text
    })
    
    # Display user message
    with st.chat_message("user", avatar='👤'):
        st.markdown(text)
    
    # Fetch response from Groq API
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

# Create tabs for different input methods
tab1, tab2 = st.tabs(["🎤 Voice Input", "⌨️ Text Input"])

with tab1:
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
                
                # Use the helper function to get summary
                get_summary_from_text(transcribed_text)
                
            else:
                st.error("❌ Transcription failed", icon="🚨")
                st.error(f"Error details: {transcribed_text}")
                
                # Show helpful installation tips
                with st.expander("🔧 Troubleshooting Tips"):
                    st.markdown("""
                    ### Common Issues and Solutions:
                    
                    1. **OpenAI Whisper not installed**:
                       ```bash
                       pip install openai-whisper
                       ```
                       - No FFmpeg required!
                       - Works with WebM, MP3, WAV, and many other formats
                       - First run downloads base model (~140 MB)
                    
                    2. **Audio too quiet or unclear**:
                       - Speak clearly and loudly
                       - Record in a quiet environment
                       - Check your microphone settings
                       - Ensure good microphone input levels
                    
                    3. **Slow transcription**:
                       - First run is slow (model download)
                       - Subsequent runs are much faster
                       - Model is cached after first use
                    
                    4. **Memory issues**:
                       - Base model is optimized for accuracy/speed balance
                       - For faster processing, you can use "tiny" model
                    """)
        else:
            st.error("Error: Could not read audio bytes")

with tab2:
    st.markdown("### ⌨️ Type Your Message")
    st.markdown("Enter your text below to get a 4-point summary using Groq LLM.")
    
    # Text input
    user_text = st.text_area(
        "Enter your text here:",
        placeholder="Type your message or paste text you want summarized...",
        height=150
    )
    
    if st.button("📝 Get Summary", type="primary"):
        if user_text.strip():
            get_summary_from_text(user_text)
            st.session_state.transcribed_text = user_text  # For display
        else:
            st.warning("Please enter some text to summarize.")

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
