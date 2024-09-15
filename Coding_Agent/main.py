# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from webhooks.handler import WebhookHandler
from agent.code_generator import CodeGenerator
from agent.code_tester import CodeTester
from agent.git_manager import GitManager

load_dotenv()

app = FastAPI(title="Git Automation Agent",
              description="An API for handling GitHub webhooks and automating code generation, testing, and pushing.")

code_generator = CodeGenerator()
code_tester = CodeTester()
git_manager = GitManager()
webhook_handler = WebhookHandler(code_generator, code_tester, git_manager)

class WebhookPayload(BaseModel):
    ref: str
    repository: dict
    pusher: dict
    # Add other fields as needed

@app.post("/webhook")
async def handle_webhook(payload: WebhookPayload, x_github_event: Optional[str] = Header(None)):
    if not x_github_event:
        raise HTTPException(status_code=400, detail="X-GitHub-Event header is missing")

    if x_github_event == 'push':
        result, status_code = webhook_handler.handle_push_event(payload.dict())
        return result
    else:
        raise HTTPException(status_code=400, detail="Unsupported event")

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()

# webhooks/handler.py
from typing import Tuple, Dict

class WebhookHandler:
    def __init__(self, code_generator, code_tester, git_manager):
        self.code_generator = code_generator
        self.code_tester = code_tester
        self.git_manager = git_manager

    def handle_push_event(self, payload: Dict) -> Tuple[Dict, int]:
        branch = payload['ref'].split('/')[-1]

        if branch == 'main':
            prompt = "Write a Python function that calculates the fibonacci sequence"
            generated_code = self.code_generator.generate_code(prompt)

            is_valid, test_output = self.code_tester.test_code(generated_code)

            if is_valid:
                file_path = 'generated_code.py'
                with open(file_path, 'w') as f:
                    f.write(generated_code)

                self.git_manager.commit_and_push(file_path, "Add generated code")
                return {'message': 'Code generated, tested, and pushed successfully'}, 200
            else:
                return {'message': 'Generated code failed tests', 'test_output': test_output}, 400

        return {'message': 'No action taken for this event'}, 200