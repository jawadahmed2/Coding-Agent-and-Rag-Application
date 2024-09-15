# main.py
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from webhooks.handler import WebhookHandler
from agent.code_generator import CodeGenerator
from agent.code_tester import CodeTester
from agent.git_manager import GitManager

load_dotenv()

app = Flask(__name__)

code_generator = CodeGenerator()
code_tester = CodeTester()
git_manager = GitManager()
webhook_handler = WebhookHandler(code_generator, code_tester, git_manager)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event == 'push':
        return webhook_handler.handle_push_event(payload)
    else:
        return jsonify({'message': 'Unsupported event'}), 400

def main():
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main()