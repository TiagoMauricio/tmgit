import subprocess

import typer
from apps.config import load_config
from helpers.constants import HELP_SYNC_CURRENT, HELP_SYNC_REPO, HELP_SYNC_WS
from helpers.exceptions import IsNotDirectory, IsNotGitRepository
from helpers.git_operations import err_console, sync_repo
from rich import print

app = typer.Typer(no_args_is_help=True)


# TODO:
# - rework ls, make it fetch directories only, move _execute to a utils helper file
# - build progress bar
# - move git operations to its own app, extract generic functions, keep private ones
@app.command(help=HELP_SYNC_WS)
def ws(name: str):
    config = load_config()
    if name in config:
        ws_location = config[name]
        dir_list = subprocess.run(
            ["ls", ws_location], capture_output=True, text=True
        ).stdout.split("\n")
        for dir in dir_list:
            # ignore empty lines
            if dir:
                repo_path = f"{config[name]}/{dir}"
                try:
                    sync_repo(repo_path)
                except IsNotDirectory:
                    print(
                        f"[yellow]WARNING[/yellow]: path {repo_path} is not a directory."
                    )
                    print(f"[green]Ignoring {repo_path}[/green]")
                except IsNotGitRepository:
                    print(
                        f"[yellow]WARNING[/yellow]: path {repo_path} is not a git repository."
                    )
                    print(f"INFO: Ignoring {repo_path}")
        return
    err_console.print("ERROR: name doesn't exist")
    exit(1)


@app.command(help=HELP_SYNC_CURRENT)
def current():
    pass


@app.command(help=HELP_SYNC_REPO)
def repo():
    pass
