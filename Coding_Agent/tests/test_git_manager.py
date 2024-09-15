# tests/test_git_manager.py
import pytest
import os
from agent.git_manager import GitManager

@pytest.fixture
def git_manager():
    return GitManager()

def test_clone_repo(git_manager):
    repo = git_manager.clone_repo()
    assert os.path.exists(git_manager.repo_path)
    assert repo.git_dir == os.path.join(git_manager.repo_path, '.git')

def test_commit_and_push(git_manager):
    test_file = 'test_file.txt'
    test_content = 'This is a test file'
    test_commit_message = 'Add test file'

    with open(os.path.join(git_manager.repo_path, test_file), 'w') as f:
        f.write(test_content)

    git_manager.commit_and_push(test_file, test_commit_message)

    repo = git_manager.clone_repo()
    assert test_file in repo.git.ls_files().split()
    assert test_commit_message in repo.git.log(max_count=1)