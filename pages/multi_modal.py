import streamlit as st
import google.generativeai as genai
from PIL import Image



gemini_api_key="AIzaSyCoe9ECLBHghslEhWH1FU94mCW62eRlryA"
st.title("📷 Multi Modal Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Gemini")

file = st.file_uploader("Choose a picture.",
                        type=["jpg", "jpeg", "png"],
                        label_visibility='collapsed')

if prompt := st.chat_input("Ask about a picture."):

    if not gemini_api_key:
        st.info("Please add your [Gemini API key](https://aistudio.google.com/app/apikey) to continue.")
        st.stop()

    genai.configure(api_key=gemini_api_key)

    if file is None:
        st.info("Please upload your picture.")
        st.stop()

    model = genai.GenerativeModel('gemini-1.5-flash')

    image = Image.open(file)
    st.image(image)

    response = model.generate_content([image, prompt])

    st.chat_message("assistant").write(response.text)
