# Groq Streamlit SummaryText App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://groqdemo.streamlit.app/)

![Demo App Screenshot](images/groq_demo.png)

This [Streamlit](https://streamlit.io/) app integrates with the [Groq API](https://groq.com/) to provide a chat interface where users can interact with advanced language models. It allows users to choose between two models for generating responses, enhancing the flexibility and user experience of the chat application.

It is blazing FAST; try it and see! 🏎️ 💨 💨 💨

**Check out the video tutorial 👇**

<a href="https://youtu.be/WQvinJGYk90">
  <img src="https://img.youtube.com/vi/WQvinJGYk90/hqdefault.jpg" alt="Watch the video" width="100%">
</a>

## Features

- **Model Selection**: Users can select between 

{
    "object": "list",
    "data": [
        {
            "id": "llama-3.1-8b-instant",
            "object": "model",
            "created": 1693721698,
            "owned_by": "Meta",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 131072
        },
        {
            "id": "meta-llama/llama-4-scout-17b-16e-instruct",
            "object": "model",
            "created": 1743874824,
            "owned_by": "Meta",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 8192
        },
        {
            "id": "qwen/qwen3-32b",
            "object": "model",
            "created": 1748396646,
            "owned_by": "Alibaba Cloud",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 40960
        },
        {
            "id": "whisper-large-v3-turbo",
            "object": "model",
            "created": 1728413088,
            "owned_by": "OpenAI",
            "active": true,
            "context_window": 448,
            "public_apps": null,
            "max_completion_tokens": 448
        },
        {
            "id": "moonshotai/kimi-k2-instruct",
            "object": "model",
            "created": 1752435491,
            "owned_by": "Moonshot AI",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 16384
        },
        {
            "id": "playai-tts",
            "object": "model",
            "created": 1740682771,
            "owned_by": "PlayAI",
            "active": true,
            "context_window": 8192,
            "public_apps": null,
            "max_completion_tokens": 8192
        },
        {
            "id": "groq/compound",
            "object": "model",
            "created": 1756949530,
            "owned_by": "Groq",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 8192
        },
        {
            "id": "openai/gpt-oss-20b",
            "object": "model",
            "created": 1754407957,
            "owned_by": "OpenAI",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 65536
        },
        {
            "id": "openai/gpt-oss-120b",
            "object": "model",
            "created": 1754408224,
            "owned_by": "OpenAI",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 65536
        },
        {
            "id": "meta-llama/llama-prompt-guard-2-86m",
            "object": "model",
            "created": 1748632165,
            "owned_by": "Meta",
            "active": true,
            "context_window": 512,
            "public_apps": null,
            "max_completion_tokens": 512
        },
        {
            "id": "allam-2-7b",
            "object": "model",
            "created": 1737672203,
            "owned_by": "SDAIA",
            "active": true,
            "context_window": 4096,
            "public_apps": null,
            "max_completion_tokens": 4096
        },
        {
            "id": "groq/compound-mini",
            "object": "model",
            "created": 1756949707,
            "owned_by": "Groq",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 8192
        },
        {
            "id": "playai-tts-arabic",
            "object": "model",
            "created": 1740682783,
            "owned_by": "PlayAI",
            "active": true,
            "context_window": 8192,
            "public_apps": null,
            "max_completion_tokens": 8192
        },
        {
            "id": "moonshotai/kimi-k2-instruct-0905",
            "object": "model",
            "created": 1757046093,
            "owned_by": "Moonshot AI",
            "active": true,
            "context_window": 262144,
            "public_apps": null,
            "max_completion_tokens": 16384
        },
        {
            "id": "llama-3.3-70b-versatile",
            "object": "model",
            "created": 1733447754,
            "owned_by": "Meta",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 32768
        },
        {
            "id": "meta-llama/llama-4-maverick-17b-128e-instruct",
            "object": "model",
            "created": 1743877158,
            "owned_by": "Meta",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 8192
        },
        {
            "id": "meta-llama/llama-guard-4-12b",
            "object": "model",
            "created": 1746743847,
            "owned_by": "Meta",
            "active": true,
            "context_window": 131072,
            "public_apps": null,
            "max_completion_tokens": 1024
        },
        {
            "id": "whisper-large-v3",
            "object": "model",
            "created": 1693721698,
            "owned_by": "OpenAI",
            "active": true,
            "context_window": 448,
            "public_apps": null,
            "max_completion_tokens": 448
        },
        {
            "id": "meta-llama/llama-prompt-guard-2-22m",
            "object": "model",
            "created": 1748632101,
            "owned_by": "Meta",
            "active": true,
            "context_window": 512,
            "public_apps": null,
            "max_completion_tokens": 512
        }
    ]
}
 models to tailor the conversation according to each model's capabilities.
- **Chat History**: The app maintains a session-based chat history, allowing for a continuous conversation flow during the app session.
- **Dynamic Response Generation**: Utilizes a generator function to stream responses from the Groq API, providing a seamless chat experience.
- **Error Handling**: Implements try-except blocks to handle potential errors gracefully during API calls.

## Requirements

- Streamlit
- Groq Python SDK
- Python 3.7+

## Setup and Installation

#create python virtual environment

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
activate the virtual environment 


- **Install Dependencies**:
pip install -r requirements.txt

  ```bash
  pip install streamlit groq
  ```

- **Set Up Groq API Key**:

  Ensure you have an API key from Groq. This key should be stored securely using Streamlit's secrets management:

  ```toml
  # .streamlit/secrets.toml
  GROQ_API_KEY="your_api_key_here"
  ```

- **Run the App**:
  Navigate to the app's directory and run:

```bash
streamlit run streamlit_app.py
```

## Usage

Upon launching the app, you are greeted with a title and a model selection dropdown.

After choosing a preferred model, you can interact with the chat interface by entering prompts.

The app displays the user's questions and the AI's responses, facilitating a back-and-forth conversation.

## Customization

The app can be easily customized to include additional language models (as Groq adds more), alter the user interface, or extend the functionality to incorporate other interactions with the Groq API.

## Contributing

Contributions are welcome to enhance the app, fix bugs, or improve documentation.

Please feel free to fork the repository, make changes, and submit a pull request.
