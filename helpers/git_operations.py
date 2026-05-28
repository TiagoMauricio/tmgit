import subprocess
from pathlib import Path
import typer

def sync_current():
    cwd_git_file = Path.cwd()/".git"
    if not cwd_git_file.exists():
        print("This is not a git repo. Abort...")
        exit(1)
    result = subprocess.run(["git","pull", "origin", "HEAD" ], capture_output=True, text=True)
    if result.returncode == 0:
        typer.echo(result.stdout)
    else:
        typer.echo(result.stderr)

