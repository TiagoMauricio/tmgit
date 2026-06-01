import json
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer
from platformdirs import PlatformDirs

import helpers.constants as constants
import helpers.git_operations as git_operations

CONFIG_FILE_NAME = "config.json"
CONFIG_DIR = Path(PlatformDirs("tmgit").user_config_dir)
CONFIG_FILE = CONFIG_DIR / CONFIG_FILE_NAME
DEFAULT_GIT_DIR = Path.home() / "git"

# print(DEFAULT_GIT_DIR)

CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# App inits
app = typer.Typer(no_args_is_help=True)


# Enums
class SyncTarget(str, Enum):
    repo = "repo"
    workspace = "ws"
    current = "current"


SYNC_TARGET_FUNCTIONS = {
    SyncTarget.current: git_operations.sync_current,
    SyncTarget.workspace: git_operations.sync_workspace,
    SyncTarget.repo: git_operations.sync_repo,
}


# Functions
def _init_config():
    return {"git_ws_dir": str(DEFAULT_GIT_DIR)}


def _load_config():
    if CONFIG_FILE.exists():
        # print(f"Loading current config file: {CONFIG_FILE}")
        return json.loads(CONFIG_FILE.read_text())

        # print(f"Config file does not exist. Creating config at: {CONFIG_FILE}")
    new_config = _init_config()
    _save_config(new_config)
    return new_config


def _save_config(config: dict):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


@app.command()
def config():
    print("Running config")


@app.command("sync")
def sync(
    target: Annotated[SyncTarget, typer.Argument(help=constants.HELP_SYNC_TARGET)],
):
    return SYNC_TARGET_FUNCTIONS[target]()

@app.command("send")
def send():
    return git_operations.send()

if __name__ == "__main__":
    _load_config()
    app()
