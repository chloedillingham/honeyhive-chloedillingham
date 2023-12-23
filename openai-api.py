from dotenv import load_dotenv
import os
from openai import *
from flask import Flask, render_template, request

# # Get the API key from the environment variables - dont adjust
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("API key is not set in the environment variables.")
client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Render the main page
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get data from form
    role = request.form['role']
    user_message = request.form['user_message']
    model = request.form['model']

    # Set up the messages for the completion request
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": role, "content": user_message}
    ]

    # Call the OpenAI API
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
    except APIError as e:
        # Handle API errors gracefully
        return render_template('index.html', generated_text=f"Error: {str(e)}")

    # Extract the assistant's response
    generated_text = response.choices[0].message.content

    # Render the page with the generated text
    return render_template('index.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)