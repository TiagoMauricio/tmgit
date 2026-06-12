import subprocess
from pathlib import Path

from helpers.exceptions import IsNotDirectory, IsNotGitRepository
from rich import print
from rich.console import Console

err_console = Console(stderr=True)


# I know functions are usually supposed to do only one thing
# however it seems a bit overkill to implement a function just
# to handle output
def _execute(command_list: list):
    print(f"[green]Executing:[/green] {command_list}")
    result = subprocess.run(command_list, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
        return result
    else:
        err_console.print(f"[red]{result.stderr}[/red]")
        exit(1)


def _check_if_git(path: str):
    cwd_git_file = Path(f"{path}/.git")
    if not cwd_git_file.exists():
        raise IsNotGitRepository


def _find_current(repo_dir: str | None = None):
    result = subprocess.run(
        "git branch --show-current".split(),
        capture_output=True,
        text=True,
        cwd=repo_dir,
    )
    if result.returncode == 0:
        return result.stdout.rstrip()
    else:
        err_console.print(
            f"[red]Failed to fetch current branch with err: {result.stderr}[/red]"
        )
        exit(1)


def _find_main(repo_dir: str | None = None):
    pass


def _commit_current(message: str):
    return _execute(["git", "commit", "-am", message])


def sync_current():
    _check_if_git(str(Path.cwd()))
    current_branch = _find_current()
    return _execute(["git", "pull", "origin", current_branch])


def sync_repo(repo_path: str):
    if not Path(repo_path).is_dir():
        raise IsNotDirectory(f"Provided path {repo_path} is not a directory.")
    _check_if_git(repo_path)
    print(f"Synching repo: {repo_path}")
    current_branch = _find_current(repo_path)
    subprocess.run(["echo", f"git pull origin {current_branch}"], cwd=repo_path)


def send(message):
    _check_if_git(str(Path.cwd()))
    if message:
        _commit_current(message)
    return _execute(["git", "push", "origin", "HEAD"])
