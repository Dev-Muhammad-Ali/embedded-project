import re
from flask import Flask, request, jsonify
from flask_cors import CORS  
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

chat_history = [
    SystemMessage(content="Your name is Jarvis and you are an AI chat bot made and owned by Muhammad Ali.")
]

def clean_text(text: str):
    if not text: 
        return ""

    text = re.sub(r"([!@#$%^&*(),.?/:;{}|<>_=+\-])\1{1,}", r"\1", text)

    text = re.sub(r"[^a-zA-Z0-9 .,!?'\-_/]", " ", text)

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text


def get_gemini_response(user_input):
    
    user_input = clean_text(user_input)

    human_message = HumanMessage(content=user_input)
    chat_history.append(human_message)

    result = llm.invoke(chat_history)
    response = result.content

    response = clean_text(response)

    ai_message = AIMessage(content=response)
    chat_history.append(ai_message)

    return response if response else "I'm not sure how to respond."


@app.route("/chat", methods=["GET"])
def chat_get():
    user_message = request.args.get("q")

    if not user_message:
        return jsonify({"error": "Please provide ?q=your_message"}), 400

    bot_response = get_gemini_response(user_message)
    return jsonify({"response": bot_response})
