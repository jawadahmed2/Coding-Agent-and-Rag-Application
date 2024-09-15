# Git Automation Agent

This project implements a coding agent capable of generating, testing, and pushing code to a dummy Git repository using webhooks for automation.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up Ollama and the Llama 3 model:

   ```bash
   ollama run llama3
   ```

3. Configure your `.env` file with the necessary credentials and settings.

4. Run the main script:

   ```bash
   python main.py
   ```

## Usage

The agent will listen for webhook events and perform the following actions:

- Generate code based on predefined prompts
- Test the generated code
- Push the code to the dummy repository
