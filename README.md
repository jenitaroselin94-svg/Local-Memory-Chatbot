# MindMate AI – Local LLM Chatbot with LangChain Memory

## Project Overview

MindMate AI is a simple AI chatbot built using a locally running Large Language Model (LLM) and LangChain conversation memory. It allows users to interact with an AI assistant while maintaining context from previous messages in the conversation.

The application uses Ollama to run the local LLM and Streamlit to provide an interactive chat interface.

## Features

- Interactive chatbot interface using Streamlit.
- Local LLM integration using Ollama.
- Supports Gemma 3:1b and Llama 3.2 models.
- LangChain conversation memory to remember previous messages.
- Maintains context during the conversation.
- Adjustable temperature setting.
- Quick prompt suggestions.
- Clear chat and memory option.
- Download chat history as a text file.
- View stored conversation memory.

## Technologies Used

- Python
- Streamlit
- LangChain
- LangChain Classic
- LangChain Core
- LangChain Ollama
- Ollama
- Gemma 3:1b
- Llama 3.2

## Project Structure

```text
MindMate AI/
│
├── app.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Navigate to the Project Folder

```bash
cd "MindMate AI"
```

### 3. Install Dependencies

```bash
py -m pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama from:

https://ollama.com/

### 5. Download the LLM Model

```bash
ollama pull gemma3:1b
```

### 6. Run the Application

```bash
py -m streamlit run app.py
```

The application will open in your web browser.
## Screenshot
<img width="1807" height="797" alt="image" src="https://github.com/user-attachments/assets/ce89a73c-0de2-489d-a40d-7797a3154397" />
<img width="1600" height="833" alt="WhatsApp Image 2026-11-06 at 13 38 37" src="https://github.com/user-attachments/assets/3433d905-129f-4d8b-b486-3c9cd65cba03" />

## How It Works

1. The user enters a message in the chatbot.
2. Streamlit receives the input.
3. LangChain manages the conversation flow.
4. Conversation memory stores recent messages.
5. Ollama sends the prompt to the locally running LLM.
6. The LLM generates a response.
7. The chatbot displays the response while retaining conversation context.

## LangChain Memory

MindMate AI uses `ConversationBufferWindowMemory` to maintain recent conversation history.

The memory window is configured with `k=5`, allowing the chatbot to use recent conversation exchanges as context when generating responses.

## Requirements

The project dependencies are listed in `requirements.txt`:

```text
streamlit
langchain
langchain-classic
langchain-core
langchain-ollama
```

## Expected Output

- A chatbot interface titled MindMate AI.
- Users can send messages and receive AI-generated responses.
- The chatbot can recall information from recent messages in the same conversation.
- Users can clear the conversation and download chat history.

## Note

This application uses a locally running Ollama model. Ollama must be installed and running on the computer to use the chatbot. Conversation memory is maintained during the active application session.
