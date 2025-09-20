import streamlit as st
from agent import agent_respond
from memory import load_memory, save_memory
from langgraph_helper import query_fact

st.set_page_config(page_title="AutonoGroq", page_icon="🤖", layout="wide")
st.title("AutonoGroq - Autonomous AI Agent")

# --- Session state for chat history (start fresh) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Optional button to load previous memory ---
if st.button("Load previous memory"):
    st.session_state.chat_history = load_memory()

# --- Ensure all old messages are dicts ---
for i, chat in enumerate(st.session_state.chat_history):
    if isinstance(chat, str):
        st.session_state.chat_history[i] = {"role": "user", "message": chat}

# --- File uploader (always on left side) ---
col1, col2 = st.columns([1, 3])
with col1:
    sales_file = st.file_uploader(
        "Upload Sales CSV/Excel/PDF file",
        type=["csv", "xlsx", "xls", "pdf"]
    )

# --- Chat input ---
user_input = st.text_input("Type your message here:")

if st.button("Send") and user_input:
    file_path = None
    if sales_file:
        file_path = f"temp_{sales_file.name}"
        with open(file_path, "wb") as f:
            f.write(sales_file.getbuffer())

    # Add user message
    st.session_state.chat_history.append({"role": "user", "message": user_input})

    # Agent response
    response = agent_respond(user_input, st.session_state.chat_history, sales_file=file_path)
    st.session_state.chat_history.append({"role": "agent", "message": response["response_text"]})

    # Save memory (optional)
    save_memory(st.session_state.chat_history)

# --- Display chat messages (user left, agent right) ---
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**You:** {chat['message']}")
    else:
        col1, col2 = st.columns([1, 3])
        with col2:
            st.markdown(f"**Agent:** {chat['message']}")
            facts = query_fact()
            if facts:
                st.markdown("**Facts remembered:**")
                for f in facts:
                    st.markdown(f"- {f[0]} — {f[1]} — {f[2]}")
