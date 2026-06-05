import json
from enum import Enum
from typing import Annotated
from rich import print

import typer

import helpers.constants as constants
import helpers.git_operations as git_operations
import helpers.config as tmconfig


# App inits
app = typer.Typer(no_args_is_help=True)
app.add_typer(tmconfig.app, name="config", help="Configure your workspaces")

# Enums
class SyncTarget(str, Enum):
    workspace = "ws"
    current = "current"

# Function Mappers
SYNC_TARGET_FUNCTIONS = {
    SyncTarget.current: git_operations.sync_current,
    SyncTarget.workspace: git_operations.sync_workspace,
}

# Functions
@app.command(help="Lists configured workspaces")
def list():
    print(tracked_workspaces)

@app.command("sync", help=constants.HELP_SYNC_COMMAND)
def sync(
    target: Annotated[SyncTarget, typer.Argument(help=constants.HELP_SYNC_TARGET)],
):
    return SYNC_TARGET_FUNCTIONS[target]()

@app.command("send", help=constants.HELP_SEND_COMMAND)
def send(message: Annotated[str, typer.Option("-m", "--message", help="Commit message to push directly to current branch.")] = None):
    return git_operations.send(message)

if __name__ == "__main__":
    tmconfig.load_config()
    app()
