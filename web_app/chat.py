import streamlit as st
import requests
import whisper
import os
import tempfile

# Initialize the Streamlit app with a dark theme
st.set_page_config(page_title="Kanna Dataset AI Chat", page_icon="🤖", layout="centered")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    .header-buttons {
        display: flex;
        justify-content: space-between;
        padding: 10px;
    }
    .header-buttons a {
        text-decoration: none;
    }
    .button-style {
        background-color: #0e76a8;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 16px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .mic-button {
        background-color: #f44336;
        color: white;
        padding: 12px 16px;
        border-radius: 50%;
        font-size: 24px;
        cursor: pointer;
    }
    .mic-button:hover {
        background-color: #d32f2f;
    }
    .footer {
        margin-top: 50px;
        padding: 20px;
        text-align: center;
        font-size: 14px;
        color: gray;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Add header with GitHub and Dataset buttons
st.markdown("<div class='header-buttons'><a href='https://github.com/yourusername/kanna-dataset' target='_blank'><button class='button-style'>GitHub</button></a><a href='https://your-dataset-link.com' target='_blank'><button class='button-style'>Dataset</button></a></div>", unsafe_allow_html=True)

# Title and description
st.title("Kanna Dataset AI Chat 🤖")
st.markdown("Welcome! Ask your questions about the Kanna dataset using either audio or text input.")

# API endpoint for generating tokens (modify as necessary)
API_URL = "http://localhost:3000"  # Change this to your actual backend URL

# Create or verify a token by calling the backend API
def get_token():
    try:
        response = requests.post(f"{API_URL}/token")  # Post request to create a new token
        if response.status_code == 201:
            return response.json().get('token', None)
        else:
            st.error("Failed to generate token. Please try again.")
            return None
    except Exception as e:
        st.error(f"Error in API request: {e}")
        return None

# Try to get the token from the backend API
token = get_token()

# Check if the token is successfully retrieved
if token:
    st.write(f"Token: {token}")
else:
    st.write("No token generated. Please refresh the page to generate a new token.")

# Fetch chat history
def get_chat_history(token):
    try:
        response = requests.get(f"{API_URL}/history?token={token}")
        if response.status_code == 200:
            return response.json().get('history', [])
        else:
            st.error("Failed to fetch chat history.")
            return []
    except Exception as e:
        st.error(f"Error in fetching history: {e}")
        return []

# Display chat history if token is available
if token:
    chat_history = get_chat_history(token)
    for chat in chat_history:
        if chat['type'] == "USER":
            st.write(f"**You:** {chat['content']}")
        elif chat['type'] == "ASSISTANT":
            st.write(f"**AI** {chat['content']}")

# Audio input (file upload for audio)
st.subheader("Upload your audio file")
audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "m4a"])

# Function to transcribe audio to text using Whisper
def transcribe_audio(audio_file):
    try:
        model = whisper.load_model("large")  # Load Whisper model (can be 'small', 'medium', or 'large')
        
        # Get the current working directory (where the script is located)
        current_directory = os.getcwd()
        
        # Define the path to save the temporary audio file in the same directory as the code
        tmp_audio_path = os.path.join(current_directory, "temp_audio.mp3")
        
        # Save the uploaded audio to this directory
        with open(tmp_audio_path, "wb") as tmp_audio_file:
            tmp_audio_file.write(audio_file.getbuffer())
        
        print(f"Temporary file created at: {tmp_audio_path}") 
        
        
        # Ensure that the file exists and the path is correct
        if os.path.exists(tmp_audio_path):
            # Transcribe the audio to text
            result = model.transcribe(tmp_audio_path, language="kn", task="translate")  # Pass the file path here
            return result['text']
        else:
            raise FileNotFoundError(f"The file at {tmp_audio_path} was not found.")
    
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None

# If an audio file is uploaded, process it
if audio_file:
    st.write(f"Audio file '{audio_file.name}' uploaded. Converting to text...")
    transcribed_text = transcribe_audio(audio_file)
    if transcribed_text:
        st.write(f"Transcribed Text: {transcribed_text}")
    else:
        st.write("Failed to transcribe the audio.")

    # Send the transcribed text to the backend API
    if token and transcribed_text:
        response = requests.post(f"{API_URL}/chat", json={"token": token, "message": transcribed_text})
        if response.status_code == 201:
            ai_response = response.json().get("assistantResponse", {}).get("content", "")
            st.write(f"**AI Response:** {ai_response}")
        else:
            st.error("Failed to get AI response.")

# Text input for question
st.subheader("Or enter your question about the Kanna dataset:")
user_question = st.text_input("Enter your question here")

# Handle text input submission
if user_question:
    if token:
        response = requests.post(f"{API_URL}/chat", json={"token": token, "message": user_question})
        if response.status_code == 201:
            result = response.json()
            st.write(f"**AI Response:** {result['assistantResponse']['content']}")
        else:
            st.error("Failed to get AI response.")
    
# Footer
st.markdown("<div class='footer'><hr><center>Powered by the Kanna Dataset</center></div>", unsafe_allow_html=True)
