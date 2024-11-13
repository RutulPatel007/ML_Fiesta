import streamlit as st

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

# Audio input (microphone button for recording)
st.subheader("Record your question as audio")
audio_value = st.audio_input("Click to record your question")

# Handle the audio input
if audio_value:
    audio_file_path = "recorded_audio.wav"
    with open(audio_file_path, "wb") as f:
        f.write(audio_value.getbuffer())  # Save the audio as bytes
    st.success(f"Audio saved as {audio_file_path}")

# Text input for question
st.subheader("Or enter your question about the Kanna dataset:")
user_question = st.text_input("Enter your question here")

# Display the user question as the response (echoing)
if user_question:
    st.write(f"**You:** {user_question}")
    st.write(f"**AI:** {user_question}")

# Footer
st.markdown("<div class='footer'><hr><center>Powered by the Kanna Dataset</center></div>", unsafe_allow_html=True)
