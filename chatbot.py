import streamlit as st
import google.generativeai as genai


with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    "[Get an Gemini API key](https://aistudio.google.com/app/apikey)"
    "[View the source code](https://github.com/danishi/streamlit-gemini-chatbot)"

st.title("✨ Gemini Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Gemini")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input("How can I help you?"):

    if not gemini_api_key:
        st.info("Please add your [Gemini API key](https://aistudio.google.com/app/apikey) to continue.")
        st.stop()

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    messages = []
    for message in st.session_state.chat_history:
        messages.append(
            {
                "role": message["role"] if message["role"] == "user" else "model",
                'parts': message["content"]
            }
        )

    response = model.generate_content(messages)

    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)
