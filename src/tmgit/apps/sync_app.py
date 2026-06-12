import subprocess

import typer
from apps.config import load_config
from helpers.constants import HELP_SYNC_CURRENT, HELP_SYNC_REPO, HELP_SYNC_WS
from helpers.exceptions import IsNotDirectory, IsNotGitRepository
from helpers.git_operations import err_console, sync_repo
from rich import print

app = typer.Typer(no_args_is_help=True)


# TODO:
# - build progress bar
# - move git operations to its own app, extract generic functions, keep private ones
@app.command(help=HELP_SYNC_WS)
def ws(name: str):
    config = load_config()
    if name in config:
        ws_location = config[name]
        repo_list = subprocess.run(
            ["find", ws_location, "-maxdepth", "1", "-type", "d"],
            capture_output=True,
            text=True,
        ).stdout.split("\n")
        # Remove the directory itself and usual empty string at the end
        repo_list.remove(ws_location)
        repo_list.remove("")
        for repo_path in repo_list:
            # ignore empty lines
            if dir:
                try:
                    sync_repo(repo_path)
                except IsNotDirectory:
                    print(
                        f"[yellow]WARNING[/yellow]: path {repo_path} is not a directory."
                    )
                    print(f"INFO: Ignoring {repo_path}")
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
