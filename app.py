import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to apply custom CSS based on the selected theme
def apply_css(theme):
    if theme == "dark":
        st.markdown("""
            <style>
            .centered-title {
                text-align: center;
                font-size: 2.5em;
                color: #1E90FF;
            }
            .user-message, .assistant-message {
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
                position: relative;
                background-color: #333;
                color: #fff;
            }
            .user-message {
                background-color: #444; /* Darker blue */
                text-align: left;
            }
            .assistant-message {
                background-color: #555; /* Darker pink */
                text-align: left;
            }
            .message-options {
                position: absolute;
                top: 5px;
                right: 10px;
                cursor: pointer;
                background: transparent;
                border: none;
                color: #fff;
            }
            .message-options-content {
                display: none;
                position: absolute;
                right: 0;
                background-color: #444;
                min-width: 120px;
                box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.5);
                z-index: 1;
            }
            .message-options-content a {
                color: #fff;
                padding: 12px 16px;
                text-decoration: none;
                display: block;
            }
            .message-options-content a:hover {background-color: #555}
            .show {display: block;}
            .tab-content {
                border: 1px solid #666;
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
            }
            .chat-history {
                border: 1px solid #666;
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
                background-color: #222;
            }
            .chat-tab {
                cursor: pointer;
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
                background-color: #333;
                transition: background-color 0.3s;
            }
            .chat-tab:hover {
                background-color: #444;
            }
            .chat-tab.active {
                background-color: #555;
            }
            .three-dots {
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
            }
            .three-dots span {
                height: 6px;
                width: 6px;
                background-color: #fff;
                border-radius: 50%;
                display: inline-block;
                margin: 0 2px;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .centered-title {
                text-align: center;
                font-size: 2.5em;
                color: #1E90FF;
            }
            .user-message, .assistant-message {
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
                position: relative;
            }
            .user-message {
                background-color: #C0E8F0;  /* Light blue */
                text-align: left;
            }
            .assistant-message {
                background-color: #F0E6EF;  /* Light pink */
                text-align: left;
            }
            .message-options {
                position: absolute;
                top: 5px;
                right: 10px;
                cursor: pointer;
                background: transparent;
                border: none;
            }
            .message-options-content {
                display: none;
                position: absolute;
                right: 0;
                background-color: #f9f9f9;
                min-width: 120px;
                box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                z-index: 1;
            }
            .message-options-content a {
                color: black;
                padding: 12px 16px;
                text-decoration: none;
                display: block;
            }
            .message-options-content a:hover {background-color: #f1f1f1}
            .show {display: block;}
            .tab-content {
                border: 1px solid #ccc;
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
            }
            .chat-history {
                border: 1px solid #ccc;
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
            .chat-tab {
                cursor: pointer;
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
                background-color: #e0e0e0;
                transition: background-color 0.3s;
            }
            .chat-tab:hover {
                background-color: #d0d0d0;
            }
            .chat-tab.active {
                background-color: #c0c0c0;
            }
            .three-dots {
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
            }
            .three-dots span {
                height: 6px;
                width: 6px;
                background-color: #333;
                border-radius: 50%;
                display: inline-block;
                margin: 0 2px;
            }
            </style>
        """, unsafe_allow_html=True)

# Set page configuration
st.set_page_config(page_title="🤖 ChatGPT-like Clone 🧠")

# Set default theme if not in session state
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

# Sidebar for theme toggle
st.sidebar.markdown("## Theme")
theme = st.sidebar.selectbox("Choose Theme", ["light", "dark"], index=0 if st.session_state["theme"] == "light" else 1)
st.session_state["theme"] = theme

# Apply CSS based on the selected theme
apply_css(st.session_state["theme"])

# Display the centered title
st.markdown('<h1 class="centered-title">🤖 ChatGPT-like Clone 🧠</h1>', unsafe_allow_html=True)

# Function to determine a context-based name for the chat
def determine_chat_context(messages):
    if not messages:
        return "Empty Chat"
    first_message = messages[0]["content"]
    context_name = first_message[:15] + "..." if len(first_message) > 15 else first_message
    return context_name

# Function to start a new chat and store the previous chat in a tab
def start_new_chat():
    if "chats" not in st.session_state:
        st.session_state.chats = []
    context_name = determine_chat_context(st.session_state.messages)
    st.session_state.chats.append({"context": context_name, "messages": st.session_state.messages})
    st.session_state.messages = []

# Sidebar button and heading for new chat
st.sidebar.markdown("## Actions")
st.sidebar.button("Start New Chat", on_click=start_new_chat)

# Display previous chats as tabs under a heading
st.sidebar.markdown("## Chat History")
if "chats" in st.session_state and st.session_state.chats:
    for i, chat in enumerate(st.session_state.chats):
        if st.sidebar.button(chat["context"], key=f"chat_{i}"):
            st.session_state.messages = chat["messages"]
            st.experimental_rerun()

# Set default OpenAI model if not in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat messages in session state if not already set
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to handle rewriting a message
def rewrite_message(index, role, content):
    st.session_state.messages[index] = {"role": role, "content": content}
    # Remove the existing assistant response
    if index + 1 < len(st.session_state.messages) and st.session_state.messages[index + 1]["role"] == "assistant":
        del st.session_state.messages[index + 1]
    # Generate new assistant response
    new_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:index + 1]]
    with st.spinner("Generating response..."):
        try:
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=new_messages,
                temperature=0.5,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.5
            )
            response_content = response['choices'][0]['message']['content']
            st.session_state.messages.insert(index + 1, {"role": "assistant", "content": response_content})
        except Exception as e:
            st.error(f"Error: {e}")
    st.experimental_rerun()

# Function to handle deleting a message
def delete_message(index):
    # Remove the message and the following assistant response
    if index + 1 < len(st.session_state.messages) and st.session_state.messages[index + 1]["role"] == "assistant":
        del st.session_state.messages[index]
        del st.session_state.messages[index]  # Remove the assistant's response
    else:
        del st.session_state.messages[index]
    st.experimental_rerun()

# Display existing chat messages
for i, message in enumerate(st.session_state.messages):
    css_class = "user-message" if message["role"] == "user" else "assistant-message"
    with st.chat_message(message["role"]):
        st.markdown(f'<div class="{css_class}">{message["content"]}</div>', unsafe_allow_html=True)
        if message["role"] == "user":
            options_key = f"options_{i}"
            if st.button("⋮", key=options_key, help="Options"):
                st.session_state.options_open = i if st.session_state.get("options_open") != i else None

            if st.session_state.get("options_open") == i:
                with st.container():
                    st.markdown('<div class="message-options-content show">', unsafe_allow_html=True)
                    if st.button("Rewrite", key=f"rewrite_{i}"):
                        st.session_state.rewrite_index = i
                        st.session_state.options_open = None
                    if st.button("Delete", key=f"delete_{i}"):
                        delete_message(i)
                        st.session_state.options_open = None
                    st.markdown('</div>', unsafe_allow_html=True)

                if st.session_state.get("rewrite_index") == i:
                    new_content = st.text_input("Edit your message:", value=message["content"], key=f"edit_{i}")
                    if st.button("Save", key=f"save_{i}"):
                        rewrite_message(i, message["role"], new_content)
                        st.session_state.pop("rewrite_index", None)

# Handle user input
if prompt := st.chat_input("💬 What is up?"):
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)

    # Generate assistant response
    with st.chat_message("assistant"):
        # Create a list of messages formatted for the OpenAI API
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        messages.append({"role": "user", "content": prompt})

        # Generate response using OpenAI client
        with st.spinner("Generating response..."):
            try:
                response = openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=messages,
                    temperature=0.5,
                    max_tokens=800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                response_content = response['choices'][0]['message']['content']
                # Display assistant response
                st.markdown(f'<div class="assistant-message">{response_content}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

    # Append assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": response_content})