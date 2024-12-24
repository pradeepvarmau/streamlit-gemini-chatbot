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
    
    # Define the healthcare prompt template
    healthcare_prompt = f"""You are a healthcare assistant. Your goal is to help users identify potential causes for their symptoms and give appropriate advice or recommendations.
    Respond politely, empathetically, and responsibly. Always encourage users to seek a healthcare professional for a proper diagnosis.
    Here's the user's symptom description:
    {prompt}

    Your response:"""
    
    # Prepare the messages for the model, including the healthcare-specific prompt
    messages = [
        {"role": "user", "parts": [healthcare_prompt]}  # Use the healthcare prompt for the user's input
    ]
    
    # Add any previous chat history if necessary
    for message in st.session_state.chat_history:
        messages.append(
            {
                "role": message["role"],  # "user" or "assistant"
                "parts": [message["content"]]  # Content inside the "parts" key
            }
        )

    try:
        # Send the prepared messages to the model for content generation
        response = model.generate_content(messages)
        
        # Add the assistant's response to the session history
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        # If an error occurs, display the error message
        st.error(f"Error generating response: {e}")
