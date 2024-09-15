# agent/git_manager.py
import os
import git
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME

class GitManager:
    def __init__(self):
        self.repo_url = f'https://{GITHUB_TOKEN}@github.com/{REPO_OWNER}/{REPO_NAME}.git'
        self.repo_path = './dummy_repo'

    def clone_repo(self):
        if not os.path.exists(self.repo_path):
            git.Repo.clone_from(self.repo_url, self.repo_path)
        return git.Repo(self.repo_path)

    def commit_and_push(self, file_path, commit_message):
        repo = self.clone_repo()
        file_path = os.path.join(self.repo_path, file_path)

        # Stage the file
        repo.index.add([file_path])

        # Commit
        repo.index.commit(commit_message)

        # Push
        origin = repo.remote(name='origin')
        origin.push()
