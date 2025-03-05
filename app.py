from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Allows frontend to talk to backend
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://nagalakshmiupadya.github.io/chatbot/"}})  # Allow all origins


# Load environment variables from .env file
load_dotenv()

# Get API key from the environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# ✅ Configure Gemini API Securely
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API key not found! Please set GEMINI_API_KEY in the .env file.")

print("API key loaded successfully!")

genai.configure(api_key=API_KEY)

# ✅ Define chatbot boundaries
SYSTEM_PROMPT = """
You are an AI chatbot for Saree Mahal, an online saree store.
1. Answer customer queries about sarees, prices, fabrics, and shopping assistance.
2. Help users negotiate discounts.
3. Reject unrelated queries by saying:
   'Sorry, I can only help with sarees and Saree Mahal-related topics.'
"""

def format_response(response_text):
    """Formats response into a structured list for better readability"""
    points = response_text.split("* ")  # Splitting based on '*' bullet points
    formatted_response = "<ul>"
    for point in points:
        if point.strip():
            formatted_response += f"<li>{point.strip()}</li>"
    formatted_response += "</ul>"
    return formatted_response

def saree_mahal_chatbot(user_input):
    """Handles chatbot responses"""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-lite")  # Use the free version
        response = model.generate_content([{"text": SYSTEM_PROMPT}, {"text": user_input}])
        return format_response(response.text.strip()) if response.text else "<p>Sorry, I didn't understand that.</p>"
    except Exception as e:
        return f"<p>An error occurred: {str(e)}</p>"

# ✅ API Endpoint for chatbot
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_input = data.get("message", "").strip()
    
    if not user_input:
        return jsonify({"response": "<p>Please enter a valid message.</p>"})

    bot_response = saree_mahal_chatbot(user_input)
    return jsonify({"response": bot_response})

# ✅ Run Flask on localhost
if __name__ == "__main__":
    app.run(debug=True)
