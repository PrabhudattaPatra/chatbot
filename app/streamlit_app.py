import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="CGU AI Assistant", page_icon="🎓")
st.title("🎓 CGU AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tool"):
            st.markdown(f"🛠️ **Tool used:** `{msg['tool']}`")

user_input = st.chat_input("Ask anything about CGU")

if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        response = requests.post(
            API_URL,
            json={
                "question": user_input,
                "thread_id": st.session_state.thread_id
            },
            timeout=60
        )

    if response.status_code != 200:
        st.error("Backend error")
    else:
        data = response.json()

        answer = data["answer"]
        tool = data["tool_used"]

        with st.chat_message("assistant"):
            st.markdown(answer)
            st.markdown(f"🛠️ **Tool used:** `{tool}`")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "tool": tool
        })
