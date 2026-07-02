from typing import Annotated

import typer

from tmgit.apps import sync_app
from tmgit.apps.config import app as tmconfig_app
from tmgit.apps.config import load_config
from tmgit.helpers import constants, git_operations

# App inits
app = typer.Typer(no_args_is_help=True)
app.add_typer(tmconfig_app, name="config", help="Configure your workspaces")
app.add_typer(sync_app.app, name="sync", help=constants.HELP_SYNC_COMMAND)


# Functions
@app.command("send", help=constants.HELP_SEND_COMMAND)
def send(
    message: Annotated[
        str | None,
        typer.Option(
            "-m", "--message", help="Commit message to push directly to current branch."
        ),
    ] = None,
):
    return git_operations.send(message)


if __name__ == "__main__":
    load_config()
    app()
