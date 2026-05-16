import json, os, time, typer
from pathlib import Path
from platformdirs import PlatformDirs
from rich.progress import track



CONFIG_FILE_NAME = "config.json"
CONFIG_DIR = Path(PlatformDirs("tmgit").user_config_dir)
CONFIG_FILE = CONFIG_DIR / CONFIG_FILE_NAME
DEFAULT_GIT_DIR = Path.home() / "git"

print(DEFAULT_GIT_DIR)

CONFIG_DIR.mkdir(parents=True, exist_ok=True)

app = typer.Typer()

def _init_config():
    return { "git_ws_dir": str(DEFAULT_GIT_DIR) }

def _load_config():
    if CONFIG_FILE.exists():
        print(f"Loading current config file: {CONFIG_FILE}")
        return json.loads(CONFIG_FILE.read_text())

    print(f"Config file does not exist. Creating config at: {CONFIG_FILE}")
    new_config = _init_config()
    _save_config(new_config)
    return new_config

def _save_config(config: dict):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

@app.command()
def config():
    print("Running config")

@app.command()
def ws_sync(workspace: str):
    print("Sync workspace...")
    total = 0
    for value in track(range(100), description="Processing..."):
        # Fake processing time
        time.sleep(0.01)
        total += 1
    print(f"Processed {total} things.")

if __name__ == "__main__":
    _load_config()
    app()
