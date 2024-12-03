import json
import random
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Chatbot:
    def __init__(self, intents_file='intents.json'):
        # Try multiple potential file paths
        possible_paths = [
            os.path.join(BASE_DIR, intents_file),  # Current directory
            os.path.join(BASE_DIR, 'templates', intents_file),  # Templates folder
            os.path.join(BASE_DIR, '..', intents_file),  # Parent directory
        ]
        
        # Default intents as fallback
        default_intents = {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["hi", "hello", "hey"],
                    "responses": ["Hello!", "Hi there!", "Greetings!"]
                },
                {
                    
                }
            ]
        }
        
        # Try to load intents from file
        self.intents = default_intents
        for path in possible_paths:
            try:
                with open(path, 'r') as file:
                    self.intents = json.load(file)
                print(f"Intents loaded successfully from {path}")
                break
            except FileNotFoundError:
                continue
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {path}")
        
        # If no file found, use default intents
        if self.intents == default_intents:
            print("Using default intents. Could not find intents.json file.")

    def get_response(self, message):
        # Convert message to lowercase
        message = message.lower()

        # Check for matching intents
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                if pattern.lower() in message:
                    return random.choice(intent['responses'])
        
        # Default response if no match found
        return "I'm not sure how to respond to that. Could you rephrase?"

app = Flask(__name__)
CORS(app)

# Initialize chatbot
chatbot = Chatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        bot_response = chatbot.get_response(user_message)
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"Error processing message: {e}")
        return jsonify({'response': 'Sorry, something went wrong.'}), 500

if __name__ == '__main__':
    # Print current working directory and script location for debugging
    print("Current Working Directory:", os.getcwd())
    print("Script Location:", BASE_DIR)
    
    app.run(debug=True, host='0.0.0.0', port=5000)