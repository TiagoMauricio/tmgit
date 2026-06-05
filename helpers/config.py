import json
import typer
from pathlib import Path
from rich import print

from platformdirs import PlatformDirs

DEFAULT_GIT_DIR = Path.home() / "git"
CONFIG_FILE_NAME = "config.json"
CONFIG_DIR = Path(PlatformDirs("tmgit").user_config_dir)
CONFIG_FILE = CONFIG_DIR / CONFIG_FILE_NAME
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

app = typer.Typer(no_args_is_help=True)

def init_config():
    return {"git_ws_dir": str(DEFAULT_GIT_DIR)}

def load_config():
    if CONFIG_FILE.exists():
        # print(f"Loading current config file: {CONFIG_FILE}")
        return json.loads(CONFIG_FILE.read_text())

    print(f"Config file does not exist. Creating config at: [green]{CONFIG_FILE}[/green]")
    new_config = init_config()
    _save_config(new_config)
    return new_config


def _save_config(config: dict):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

def add():
    pass

def remove():
    pass

def edit():
    pass
