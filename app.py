import streamlit as st
from datetime import datetime

from langchain_ollama import ChatOllama
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="MindMate AI",
    page_icon="🧠",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0f2fe, #ede9fe);
}

h1 {
    color: #4338ca;
    font-weight: 800;
}

h2, h3 {
    color: #5b21b6;
}

[data-testid="stChatMessage"] {
    background: white;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #ddd6fe;
}

.stButton button {
    background: #6366f1;
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton button:hover {
    background: #4338ca;
    color: white;
}

[data-testid="stSidebar"] {
    background: #ede9fe;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# SESSION STATE
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(
        k=5,
        memory_key="chat_history",
        input_key="question",
        output_key="answer",
        return_messages=False
    )

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# --------------------------------
# LOAD LOCAL LLM
# --------------------------------

@st.cache_resource
def load_model(model_name, temperature):
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        base_url="http://localhost:11434"
    )

# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.title("🧠 MindMate AI")

    st.write("Your Smart AI Companion")

    st.divider()

    st.subheader("⚙️ AI Settings")

    model_name = st.selectbox(
        "Choose LLM Model",
        ["gemma3:1b", "llama3.2:latest"]
    )

    temperature = st.slider(
        "Response Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    st.divider()

    st.subheader("🧠 Memory Settings")

    st.info(
        "MindMate remembers your latest "
        "5 conversation exchanges."
    )

    if st.button("🗑️ Clear Chat & Memory",
                 use_container_width=True):

        st.session_state.messages = []
        st.session_state.memory.clear()

        st.rerun()

    st.divider()

    st.subheader("📊 Chat Statistics")

    st.metric(
        "Total Messages",
        len(st.session_state.messages)
    )

    st.metric(
        "User Questions",
        sum(
            1 for m in st.session_state.messages
            if m["role"] == "user"
        )
    )

    st.divider()

    st.caption("Powered by Ollama & LangChain")

# --------------------------------
# MAIN INTERFACE
# --------------------------------

st.title("🧠 MindMate AI")

st.markdown(
    "**Think • Learn • Remember**"
)

st.write(
    "Your intelligent AI assistant "
    "that remembers your conversations."
)

st.divider()

# --------------------------------
# QUICK PROMPTS
# --------------------------------

st.subheader("💡 Quick Questions")

col1, col2, col3 = st.columns(3)

if col1.button("Explain AI"):
    st.session_state.pending_prompt = (
        "Explain Artificial Intelligence in simple words."
    )
    st.rerun()

if col2.button("Python Help"):
    st.session_state.pending_prompt = (
        "Teach me Python programming with an example."
    )
    st.rerun()

if col3.button("Study Tips"):
    st.session_state.pending_prompt = (
        "Give me effective study tips for computer science."
    )
    st.rerun()

st.divider()

# --------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------
# CHAT INPUT
# --------------------------------

user_input = st.chat_input(
    "Ask MindMate anything..."
)

if st.session_state.pending_prompt:

    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# --------------------------------
# GENERATE RESPONSE
# --------------------------------

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    try:

        llm = load_model(model_name, temperature)

        memory = st.session_state.memory

        history = memory.load_memory_variables({})

        prompt = ChatPromptTemplate.from_messages([

            (
                "system",
                """
                You are MindMate AI.

                You are a friendly, intelligent
                and helpful AI assistant.

                Remember previous conversations.

                Give clear and simple answers.

                Help users with programming,
                education and general questions.
                """
            ),

            (
                "human",
                """
                Previous Conversation:
                {chat_history}

                Current Question:
                {question}
                """
            )
        ])

        chain = prompt | llm

        with st.chat_message("assistant"):

            with st.spinner("MindMate is thinking..."):

                response = chain.invoke({
                    "chat_history": history["chat_history"],
                    "question": user_input
                })

                answer = response.content

                st.markdown(answer)

        # SAVE CONVERSATION IN MEMORY

        memory.save_context(
            {"question": user_input},
            {"answer": answer}
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:

        st.error(f"AI Error: {e}")

        st.info(
            "Check Ollama and make sure "
            "your selected model is installed."
        )

# --------------------------------
# DOWNLOAD CHAT HISTORY
# --------------------------------

st.divider()

st.subheader("📥 Export Conversation")

if st.session_state.messages:

    chat_text = "MINDMATE AI - CHAT HISTORY\n\n"

    for message in st.session_state.messages:

        role = message["role"].upper()

        chat_text += f"{role}:\n"
        chat_text += message["content"] + "\n\n"

    st.download_button(
        label="Download Chat History",
        data=chat_text,
        file_name="MindMate_Chat_History.txt",
        mime="text/plain"
    )

else:

    st.caption("Start chatting to export your conversation.")

# --------------------------------
# MEMORY VIEWER
# --------------------------------

with st.expander("🧠 View Conversation Memory"):

    memory_data = st.session_state.memory.load_memory_variables({})

    st.write("Recent Conversation Memory:")

    st.write(
        memory_data.get(
            "chat_history",
            "No memory available yet."
        )
    )

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.markdown(
    "<center>Made with Python, Streamlit, "
    "Ollama and LangChain</center>",
    unsafe_allow_html=True
)
