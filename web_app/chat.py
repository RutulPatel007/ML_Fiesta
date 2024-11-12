import streamlit as st
from transformers import pipeline

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
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Add header with GitHub and Dataset buttons
st.markdown("<div class='header-buttons'><a href='https://github.com/yourusername/kanna-dataset' target='_blank'><button style='background-color:#0e76a8;color:white;padding:10px 20px;border-radius:8px;'>GitHub</button></a><a href='https://your-dataset-link.com' target='_blank'><button style='background-color:#1db954;color:white;padding:10px 20px;border-radius:8px;'>Dataset</button></a></div>", unsafe_allow_html=True)

st.title("Kanna Dataset AI Chat 🤖")

# Load the question-answering model (can be replaced with your fine-tuned model)
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Chat function
def get_answer(question, context=""):
    response = qa_pipeline(question=question, context=context)
    return response["answer"]

# Text input for question
st.subheader("Ask me anything about the Kanna dataset:")
user_question = st.text_input("Enter your question here")

# Display chat conversation
if user_question:
    # Placeholder for the Kanna dataset context
    kanna_context = "This is the context or description of the Kanna dataset. Replace this with the actual dataset content or a summary."

    # Get answer from model
    answer = get_answer(user_question, context=kanna_context)

    # Display Q&A
    st.write(f"**You:** {user_question}")
    st.write(f"**AI:** {answer}")

# Add footer text
st.markdown("<hr><center>Powered by the Kanna Dataset</center>", unsafe_allow_html=True)
