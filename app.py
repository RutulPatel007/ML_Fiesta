import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from google.ai.generativelanguage import Content, Part
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Retrieve API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=API_KEY)  # Configure the API key

# Initialize the Google Gemini model
llm = genai.GenerativeModel("gemini-1.5-flash")  # Simplified initialization

# Define the prompt for generating question-answer pairs from a paragraph
dataset_creation_template = '''You are an assistant creating a JSON-format question-answer dataset.
For the following paragraph, generate a set of questions and answers that each focus on a different key point within the paragraph.
Each question should contain enough specific context about the subject (e.g., names, key details) so that the question is understandable on its own without additional background knowledge.
Make sure the question explicitly mentions the subject being discussed (e.g., tree's name, key features, or location).

Output each pair in the following JSON structure:
{
  "instruction": "A clear question that contains all relevant context from the paragraph (e.g., name of the object, key attributes, etc.)",
  "input": let this field be empty string
  "output": "A concise answer based on the paragraph"
}

Here is the paragraph:
{paragraph}

Please create question-answer pairs that are clear, self-contained, and provide all necessary context in the questions.'''

# Create a structured prompt using ChatPromptTemplate
prompt_for_dataset_creation = ChatPromptTemplate.from_messages(
    [
        ("system", dataset_creation_template),
        ("user", "{paragraph}")
    ]
)

# Initialize the output parser
parser_for_dataset_creation = StrOutputParser()

def create_qa_dataset_from_paragraph(input_file="input.txt", output_file="output.txt"):
    try:
        # Open input file with encoding 'utf-8' to avoid encoding issues
        with open(input_file, "r", encoding="utf-8") as file:
            paragraph = file.read().strip()
        
        if not paragraph:
            print("Input file is empty.")
            return

        # Prepare the content parts with the paragraph
        content_parts = [
            Part(text=dataset_creation_template),  # System message with instructions
            Part(text=paragraph)  # Reference paragraph
        ]

        # Generate the content
        response = llm.generate_content(Content(parts=content_parts), stream=False)

        # Check if the response is empty
        if not response or not response.text:
            print("The response is empty. Please check the API configuration or input data.")
            return

        # Debug: Print raw response text
        print("Raw response:", response.text)

        # Parse the AI's response into question-answer pairs
        parsed_response = parser_for_dataset_creation.invoke(response.text)

        # Debug: Print parsed response
        print("Parsed response:", parsed_response)

        # Process each question-answer pair and write to .txt file
        qa_pairs = []
        lines = parsed_response.splitlines()
        for i in range(0, len(lines), 2):
            if lines[i].startswith("Q: ") and lines[i + 1].startswith("A: "):
                question = lines[i][3:].strip()
                answer = lines[i + 1][3:].strip()
                qa_pairs.append({
                    "instruction": question,
                    "output": answer
                })

        # Append the new Q&A pairs to the output file with 'utf-8' encoding
        with open(output_file, "a", encoding="utf-8") as file:
            for pair in qa_pairs:
                file.write(json.dumps(pair, indent=4) + ",\n")  # Write each pair on a new line with JSON format

        print("Question-answer dataset has been appended to output.txt")

    except FileNotFoundError:
        print("The input file does not exist.")
    except UnicodeDecodeError as e:
        print(f"Unicode decode error: {e}. Try using a different encoding.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# Call the function to generate a question-answer dataset and append it to the output .txt file
create_qa_dataset_from_paragraph()
