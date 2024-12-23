import streamlit as st
import google.generativeai as genai

# Ensure you input the Gemini API key for your Google Generative AI model
gemini_api_key = "AIzaSyCoe9ECLBHghslEhWH1FU94mCW62eRlryA"  # Replace with your actual API key

# Set up the Streamlit app
st.title("✨ Healthcare Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Gemini to assist with healthcare-related queries.")

# Initialize the session state for chat history if it's not already initialized
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display the chat history for conversation
for message in st.session_state.chat_history:
    st.chat_message(message["role"]).write(message["content"])

# If the user submits a prompt, process the input
if prompt := st.chat_input("Ask me anything about healthcare!"):
    
    # Check if the Gemini API key is provided
    if not gemini_api_key:
        st.info("Please add your [Gemini API key](https://aistudio.google.com/app/apikey) to continue.")
        st.stop()
    
    # Configure the API with your key
    genai.configure(api_key=gemini_api_key)
    
    # Use the Gemini model (make sure to replace with the correct model name if necessary)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Add the user message to the session history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Prepare the healthcare-specific prompt for the model
    healthcare_prompt = f"""
    You are a healthcare assistant trained to provide clear, accurate, and empathetic medical information. 
    Your responses should be focused on healthcare-related topics such as medical conditions, treatment options, preventive care, and general wellness.
    Please provide evidence-based information that is simple to understand for a wide audience, ensuring to explain complex medical terms when necessary.
    If asked about a specific condition, describe the symptoms, causes, diagnostic process, and possible treatment options.
    Avoid giving personal medical advice, but offer reliable information that can guide the user in seeking professional care.

    User Query: {prompt}
    """

    # Add the healthcare prompt to the message list for the model
    messages = [{"role": "system", "content": healthcare_prompt}]  # Adding healthcare context to the system message

    # Add the user’s input message to the context
    for message in st.session_state.chat_history:
        messages.append(
            {
                "role": message["role"] if message["role"] == "user" else "model",
                "content": message["content"]
            }
        )

    # Send the prepared messages to the model for content generation
    response = model.generate_content(messages)
    
    # Add the assistant's response to the session history
    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)
