import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

load_dotenv()

def generate_text(prompt):
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
    response = llm.invoke(prompt)
    return response.content

def generate_code(prompt):
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2)
    messages = [
        HumanMessage(content=f"You are a helpful coding assistant. Generate code for the following prompt: {prompt}"),
    ]
    response = llm.invoke(messages)
    return response.content

def classify_text(text, categories):
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    prompt = f"Classify the following text: '{text}' into one of the following categories: {', '.join(categories)}. Only return the category name."
    messages = [
        HumanMessage(content=prompt),
    ]
    response = llm.invoke(messages)
    return response.content