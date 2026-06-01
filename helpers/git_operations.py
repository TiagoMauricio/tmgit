import subprocess
from pathlib import Path
from turtle import resetscreen
from rich import print

import typer

#TODO: add a function to handle output

def _execute(command_string: str):
    print(f"[green]Executing:[/green] {command_string}")
    result = subprocess.run(command_string.split(), capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
        return(result)
    else:
        print(f"[red]{result.stderr}[/red]")
        exit(1)


def _check_if_git():
    cwd_git_file = Path.cwd() / ".git"
    if not cwd_git_file.exists():
        print("[red]This is not a git repo. Abort...[/red]")
        exit(1)


def _fetch_current():
    result = subprocess.run("git branch --show-current".split(), capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.rstrip()
    else:
        print(f"[red]Failed to fetch current branch with err: {result.stderr}[/red]")
        exit(1)

def sync_current():
    _check_if_git()
    current_branch = _fetch_current()
    return _execute(f"git pull origin {current_branch}")


def sync_workspace():
    print("this is sync workspace")


def sync_repo():
    print("this is sync repo")

#TODO: handle output
def send():
    _check_if_git()
    return _execute("git push origin HEAD")
