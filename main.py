import json, os, time, typer, subprocess
import helpers.constants as constants, helpers.git_operations as git_operations
from pathlib import Path
from platformdirs import PlatformDirs
from rich.progress import track
from typing import Annotated
from enum import Enum


CONFIG_FILE_NAME = "config.json"
CONFIG_DIR = Path(PlatformDirs("tmgit").user_config_dir)
CONFIG_FILE = CONFIG_DIR / CONFIG_FILE_NAME
DEFAULT_GIT_DIR = Path.home() / "git"

#print(DEFAULT_GIT_DIR)

CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# App inits
app = typer.Typer(no_args_is_help=True)

# Enums
class SyncTarget(str, Enum):
    repo = "repo"
    ws   = "ws"
    current = "current"

# Functions
def _init_config():
    return { "git_ws_dir": str(DEFAULT_GIT_DIR) }

def _load_config():
    if CONFIG_FILE.exists():
        #print(f"Loading current config file: {CONFIG_FILE}")
        return json.loads(CONFIG_FILE.read_text())

        #print(f"Config file does not exist. Creating config at: {CONFIG_FILE}")
    new_config = _init_config()
    _save_config(new_config)
    return new_config

def _save_config(config: dict):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

@app.command()
def config():
    print("Running config")

@app.command("sync")
def sync(target: Annotated[SyncTarget, typer.Argument(help=constants.HELP_SYNC_TARGET)]):
    if target == "current":
        return git_operations.sync_current()
if __name__ == "__main__":
    _load_config()
    app()
