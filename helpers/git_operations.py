import subprocess
from pathlib import Path
from turtle import resetscreen

import typer


def _execute(*args):
    result = subprocess.run(*args)
    if result.returncode == 0:
        typer.echo(result.stdout)
    else:
        typer.echo(result.stderr)


def _check_if_git():
    cwd_git_file = Path.cwd() / ".git"
    if not cwd_git_file.exists():
        print("This is not a git repo. Abort...")
        exit(1)


def _fetch_current():
    return "main"


def sync_current():
    _check_if_git()
    return _execute("git", "pull", "origin", _fetch_current())


def sync_workspace():
    print("this is sync workspace")


def sync_repo():
    print("this is sync repo")
