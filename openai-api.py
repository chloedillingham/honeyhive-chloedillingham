from dotenv import load_dotenv
import os
from openai import *
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
import secrets

# # Get the API key from the environment variables - dont adjust
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("API key is not set in the environment variables.")
client = OpenAI(api_key=api_key)

app = Flask(__name__)
# Configure the secret key for sessions
app.config['SECRET_KEY'] = secrets.token_hex(16)  
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/', methods=['GET'])
def index():
    session['conversation'] = []
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    # Retrieve the user message and model from the request
    user_message = data['message']
    model = data.get('model', 'gpt-4')  # Default to a specific model

    # Initialize conversation history if it doesn't exist
    if 'conversation' not in session:
        session['conversation'] = []

    # Append the user's message to the conversation history
    session['conversation'].append({"role": "user", "content": user_message})

    # Call the OpenAI API
    try:
        response = client.chat.completions.create(
            model=model,
            messages=session['conversation']
        )
    except APIError as e:
        # Handle API errors gracefully
        return jsonify({'error': str(e)})

    # Extract the assistant's response and append it to the conversation
    generated_text = response.choices[0].message.content
    print(generated_text)
    session['conversation'].append({"role": "assistant", "content": generated_text})

    # Return the generated text as JSON
    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(debug=True)