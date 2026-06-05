import json
import typer
from pathlib import Path
from rich import print
from rich.pretty import pprint
from rich.table import Table
from rich.console import Console

from platformdirs import PlatformDirs

DEFAULT_GIT_DIR = Path.home() / "git"
CONFIG_FILE_NAME = "config.json"
CONFIG_DIR = Path(PlatformDirs("tmgit").user_config_dir)
CONFIG_FILE = CONFIG_DIR / CONFIG_FILE_NAME
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

err_console = Console(stderr=True)
app = typer.Typer(no_args_is_help=True)

def _init_config():
    return {"git_ws_dir": str(DEFAULT_GIT_DIR)}

def _save_config(config: dict):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())

    err_console.print(f"Config file does not exist. Creating config at: [green]{CONFIG_FILE}[/green]")
    new_config = _init_config()
    _save_config(new_config)
    return new_config

@app.command()
def show():
    config = load_config()
    table = Table("Workspace", "Path")
    for workspace, path in config.items():
        table.add_row(workspace, path)
    print(table)

@app.command()
def add(name: str, path: Path):
    if not path.exists():
        print(f"[red]ERROR:[/red] Workspace directory '{path}' does not exist.")
        exit(1)
    config = load_config()
    config[name] = str(path)
    _save_config(config)
    show()

@app.command()
def remove(name: str):
    config = load_config()
    if name in config:
        del config[name]
        print(f"[green]SUCCESS:[/green] Removed workspace {name} from config.")
        _save_config(config)
    else:
        err_console.print(f"[red]ERROR:[/red] Config does not contain a workspace with name {name}")
        show()

@app.command()
def edit(name: str, path: Path):
    config = load_config()
    if not path.exists():
        print(f"[red]ERROR:[/red] Workspace directory '{path}' does not exist.")
        exit(1)
    elif not name in config:
        err_console.print(f"[red]ERROR:[/red] Workspace {name} it not configured. Use 'tmgit config add NAME PATH' to configure.")
        exit(1)
    config[name] = str(path)
    _save_config(config)
    print(f"[green]SUCCESS:[/green]: Workspace {name} was edited.")
    show()
