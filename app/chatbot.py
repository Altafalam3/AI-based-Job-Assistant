import os
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

def initialize_session_state():
    """
    Initialize the session state variables if they don't exist.
    """
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'model' not in st.session_state:
        st.session_state.model = 'llama-3.1-70b-versatile'

def display_customization_options():
    """
    Add customization options to the sidebar for model selection.
    """
    st.sidebar.title('Customization')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'whisper-large-v3', 'distil-whisper-large-v3-en', 'mixtral-8x7b-32768', 'gemma-7b-it'],
        key='model_selectbox'
    )
    return model

def initialize_groq_chat(groq_api_key, model):
    """
    Initialize the Groq Langchain chat object.
    """
    return ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model
    )

def initialize_conversation(groq_chat, memory):
    """
    Initialize the conversation chain with the Groq chat object and memory.
    """
    return ConversationChain(
        llm=groq_chat,
        memory=memory
    )

def process_user_question(user_question, conversation):
    """
    Process the user's question and generate a response using the conversation chain.
    """
    response = conversation(user_question)
    st.session_state.chat_history[-1]["AI"] = response['response']

def display_chat_history():
    """
    Display the chat history, including both user questions and AI responses.
    """
    chat_history_container = st.container()

    with chat_history_container:
        st.write(
            "<div style='height: 400px; overflow-y: auto; padding-right: 10px;'>",
            unsafe_allow_html=True,
        )
        for message in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(message['human'])
            if message['AI']:
                with st.chat_message("assistant"):
                    st.markdown(message['AI'])
        st.write("</div>", unsafe_allow_html=True)

def main():
    """
    The main entry point of the application.
    """
    groq_api_key = os.environ['GROQ_API_KEY']

    initialize_session_state()

    st.title("Lightning ⚡️")
    st.markdown("Chat with Lightning, an ultra-fast AI chatbot powered by Groq LPUs!")

    model = display_customization_options()

    if st.session_state.model != model:
        # Reset chat history and session state when the model is switched
        st.session_state.chat_history = []
        st.session_state.model = model
        st.experimental_rerun()

    # Use ConversationBufferMemory for infinite memory until refresh
    memory = ConversationBufferMemory()

    st.divider()
    if user_question := st.chat_input("What is up?"):
        # Add user message to the chat history before processing
        st.session_state.chat_history.append({"human": user_question, "AI": ""})

        groq_chat = initialize_groq_chat(groq_api_key, model)
        conversation = initialize_conversation(groq_chat, memory)

        # Save the entire chat context to memory before generating a response
        for message in st.session_state.chat_history:
            memory.save_context({'input': message['human']}, {'output': message['AI']})

        process_user_question(user_question, conversation)

    # Display the chat history including both the user's questions and AI responses
    display_chat_history()

if __name__ == "__main__":
    main()
