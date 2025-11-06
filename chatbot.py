import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os

# Load environment variables
load_dotenv()

# ✅ Use correct environment variable name (Groq expects GROQ_API_KEY)
os.environ["GROQ_API_KEY"] = os.getenv("api_key", "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")

# Streamlit page setup
st.set_page_config(page_title="Chatbot")
st.title("💬 Chatbot")

# Sidebar configuration
model_name = st.sidebar.selectbox(
    "Please select your Groq model:",
    ["qwen/qwen3-32b", "llama-3.1-8b-instant", "openai/gpt-oss-20b"]
)

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_token = st.sidebar.slider("Max Tokens", 50, 2000, 256)

# ✅ Initialize memory only once
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# ✅ Keep track of chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input
user_input = st.chat_input("You:")

if user_input:
    # Add user input to history
    st.session_state.history.append(("user", user_input))

    # Initialize Groq LLM
    llm = ChatGroq(
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_token
    )

    # Create conversation chain
    conv = ConversationChain(
        llm=llm,
        memory=st.session_state.memory,
        verbose=True
    )

    # Get AI response
    ai_response = conv.predict(input=user_input)

    # Save AI response
    st.session_state.history.append(("assistant", ai_response))

# ✅ Display chat messages properly
for role, text in st.session_state.history:
    if role == "user":
        st.chat_message("user").write(text)
    else:
        st.chat_message("assistant").write(text)
