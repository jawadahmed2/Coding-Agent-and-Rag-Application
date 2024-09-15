# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('REPO_OWNER')
REPO_NAME = os.getenv('REPO_NAME')
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL')