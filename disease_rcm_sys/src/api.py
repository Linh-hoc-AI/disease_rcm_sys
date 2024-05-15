from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import random
from train_agent import DQN
from environment import Env
import os
from datetime import datetime
import json

# Khởi tạo môi trường

# env = Env()
# input_size = env.state_embed_size

# Khởi tạo mô hình

# model = DQN(input_size)  # Truyền input_size vào hàm khởi tạo của model
# model.load_state_dict(torch.load("dqn-policy.pt"))
# model.eval()
# print(model)

# Khởi tạo server
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET', 'POST'])
def run_server():
    return "Hihi Haha Huhu =))"

@app.route('/inference', methods=['GET', 'POST'])
def inference():
    return f"Random number: {int(random.uniform(0, 10))}"

MESSAGES_FILE = 'messages.json'

# Utility function to read messages from the file
def read_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, 'r') as file:
        return json.load(file)

# Utility function to write messages to the file
def write_messages(messages):
    with open(MESSAGES_FILE, 'w') as file:
        json.dump(messages, file, indent=2)

# Utility function to clear messages file
def clear_messages():
    if os.path.exists(MESSAGES_FILE):
        os.remove(MESSAGES_FILE)

@app.route('/save_messages_history', methods=['POST', 'GET'])
def save_messages_hisory():
    data = request.get_json()
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    messages = read_messages()
    messages.append({
        'message': message,
        'timestamp': datetime.now().isoformat()
    })

    write_messages(messages)

    return jsonify({'success': True, 'message': 'Message stored successfully'})

@app.route('/clear_messages_history', methods=['POST'])
def clear_message_history():
    clear_messages()
    return jsonify({'success': True, 'message': 'Message history cleared'})

if __name__ == "__main__":
    app.run(host="0.0.0.0")