import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
import os
from langchain.chains import ConversationChain

load_dotenv()

os.environ["api_key"]=os.getenv("api_key","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")


st.set_page_config(page_title="Chatbot")

st.title("Chatbot")

model_name = st.sidebar.selectbox("please select your Groq model",["qwen/qwen3-32b","llama-3.1-8b-instant","openai/gpt-oss-20b"])

temperature= st.sidebar.slider("Temperature", 0.0,0.1,0.7)
max_token= st.sidebar.slider("Max Token",50,100,150)

if "memory" not in st.session_state:
    st.session_state.memory =ConversationBufferMemory(return_message=True)

if "history" not in st.session_state:
    st.session_state.history =[]


user_input= st.chat_input("you:")

if user_input:
    st.session_state.history.append(("user",user_input))
    llm= ChatGroq(model_name=model_name,temperature=temperature,max_token=max_token)

conv= ConversationChain(llm=llm,memory=st.session_state.memory,verbose=True)

ai_response=conv.predict(user=user_input)

st.session_state.history.append(("Assistant",ai_response))

for role,text in st.session_state.append:
    if role=="user":
        st.chat_message('user').write(text)
    else:  
       st.chat_message("assistant").write(text)