from dotenv import load_dotenv
import os
from openai import *
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
import secrets
import base64

# Get the API key from the environment variables - don't adjust
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
    # Initialize or clear the conversation history
    session['conversation'] = []
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_message = request.form['message']
    model = request.form['model']

    # Initialize conversation history if it doesn't exist
    if 'conversation' not in session:
        session['conversation'] = []

    # Append the user's message to the conversation history
    session['conversation'].append({"role": "user", "content": user_message})

    # Prepare the messages payload for the API
    messages_payload = session['conversation'].copy()

    if 'image' in request.files and model == 'gpt-4-vision-preview':
        image = request.files['image']
        base64_image = base64.b64encode(image.read()).decode('utf-8')

        # Append the image information to the last message in the conversation
        messages_payload[-1]["content"] = [
            {"type": "text", "text": user_message},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]

    # Call the OpenAI API
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages_payload,
            max_tokens=300
        )
    except Exception as e:
        # Handle exceptions and errors
        return jsonify({'error': str(e)})

    # Extract the generated text
    generated_text = response.choices[0].message.content

    # Append the bot's response to the conversation
    session['conversation'].append({"role": "assistant", "content": generated_text})

    # Return the generated text as JSON
    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(debug=True)
