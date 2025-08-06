import streamlit as st
import google.generativeai as genai
import pdfplumber
#import docx
import tempfile
import os

st.title("Welcome To Your Legal Document Analyzer")
st.write("This application will help you analyze legal documents and provide insights based on the content.")
communication_style=st.text_input("Please enter the style of communication you'd like to use:")
description=st.text_input("Describe the problem or thing you'd like to review in the document:")
file=st.file_uploader("Upload document",type=["pdf","txt"])
st.sidebar.header("Legal Document Analyzer Sidebar")
st.sidebar.markdown("This AI, Johnny, will serve as an assistant to explain and analyze any documents you'd like to upload.")
st.sidebar.markdown("You can input specifics asking the AI to summarize, find solutions, or explain key things in the document.")
st.sidebar.markdown("Johnny will also act based on your own inputted communication style to best suit your needs.")

genai.configure(api_key="AIzaSyCUKjgt_xXR29xzPvhRFufoozCPHzok2iY")
model=genai.GenerativeModel("gemini-2.5-flash")

def extract_text(file):
    file_ext = file.name.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
        tmp.write(file.read())
        temp_path = tmp.name
    text = ""
    if file_ext == "pdf":
        with pdfplumber.open(temp_path) as pdf:
            text = "\n\n".join([page.extract_text() or "" for page in pdf.pages])
    #elif file_ext == "docx":
        #doc = docx.Document(temp_path)
        #text = "\n".join([para.text for para in doc.paragraphs])
    elif file_ext == "txt":
        with open(temp_path, "r", encoding="utf-8") as f:
            text = f.read()
    os.remove(temp_path)
    return text.strip()

if st.button("Analyze Document"):
    if file:
        doc_text = extract_text(file)
    if not doc_text:
        st.warning("Please paste some text or upload a document to analyze.")
    else:
        with st.spinner("Analyzing document with Gemini..."):
            prompt=f"""
You are Johnny, an AI buisness assisstant designed to help with tasks such as scanning the user inputted document {file}.
You respond in a {communication_style} way.
You will be provided text inputs in natural language. Interpret them as business-related queries and respond with clarity, actionability, and confidence.
Ask follow-up questions only when necessary, and always aim to lighten the user’s workload.
Your role is to act as a trusted, efficient, and proactive business partner who can support decision-making, manage workflows, and improve productivity.
Give a detailed description of the solution to this problem in an elaborate manner: {description}
"""
    text1=model.generate_content([prompt])
    st.write(text1.text)
