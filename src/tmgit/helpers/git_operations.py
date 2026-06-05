import subprocess
from pathlib import Path
from turtle import resetscreen
from rich import print
from rich.console import Console

import typer

err_console = Console(stderr=True)

# I know functions are usually supposed to do only one thing
# however it seems a bit overkill to implement a function just
# to handle output
def _execute(command_list: list):
    print(f"[green]Executing:[/green] {command_list}")
    result = subprocess.run(command_list, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
        return(result)
    else:
        err_console.print(f"[red]{result.stderr}[/red]")
        exit(1)


def _check_if_git():
    cwd_git_file = Path.cwd() / ".git"
    if not cwd_git_file.exists():
        err_console.print("[red]This is not a git repo. Abort...[/red]")
        exit(1)


def _fetch_current():
    result = subprocess.run("git branch --show-current".split(), capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.rstrip()
    else:
        err_console.print(f"[red]Failed to fetch current branch with err: {result.stderr}[/red]")
        exit(1)

def _commit_current(message: str):
    return _execute(["git", "commit", "-am", message])

def sync_current():
    _check_if_git()
    current_branch = _fetch_current()
    return _execute(["git", "pull", "origin", current_branch])


def sync_workspace():
    print("this is sync workspace")


def sync_repo():
    print("this is sync repo")

def send(message):
    _check_if_git()
    if message:
        _commit_current(message)
    return _execute(["git", "push", "origin", "HEAD"])
