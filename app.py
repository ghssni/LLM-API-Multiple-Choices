import requests
import fitz
import streamlit as st

# Function to load and read document
def load_document(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to consume cakra.ai LLM API
def get_llm_response(text, token):
    url = "https://saas.cakra.ai/genv2/llms"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "model_name": "brain-v2",
        "messages": [
            {"role": "system", "content": "Your Chatbot AI Assistant"},
            {"role": "user", "content": f"berikan 5 pertanyaan dengan pilihan ganda ABCD dalam bahasa Indonesia:\n{text}"}
        ],
        "max_new_tokens": 300,
        "do_sample": False,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 1.0
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to format response into multiple-choice questions
def format_questions(response):
    content = response['choices'][0]['content']
    questions = content.split('\n\n')
    formatted_questions = []
    for question in questions:
        if question:
            parts = question.split('\n')
            question_text = parts[0]
            options = parts[1:5]
            formatted_questions.append((question_text, options))
    return formatted_questions[:5]

# Streamlit UI
st.title("LLM API Multiple-Choice Question Generator")
uploaded_file = st.file_uploader("Upload your story PDF", type=["pdf"])
token = st.text_input("Enter your API token")

if uploaded_file and token:
    doc_text = load_document(uploaded_file)
    response = get_llm_response(doc_text, token)
    questions = format_questions(response)

    st.write("Generated Questions:")
    for i, (q, choices) in enumerate(questions):
        st.write(f"{i+1}. {q}")
        for choice in choices:
            st.write(choice)
