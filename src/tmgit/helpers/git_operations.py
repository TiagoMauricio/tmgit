import subprocess
from pathlib import Path

from rich import print
from rich.console import Console

from tmgit.helpers.exceptions import ExecutionError, IsNotDirectory, IsNotGitRepository

err_console = Console(stderr=True)


# I know functions are usually supposed to do only one thing
# however it seems a bit overkill to implement a function just
# to handle output
def _execute(command_list: list, work_dir: str | None = str(Path.cwd())):
    # print(f"[green]Executing:[/green] {command_list}")
    result = subprocess.run(command_list, cwd=work_dir, capture_output=True, text=True)
    if result.returncode == 0:
        # print(result.stdout)
        return result
    else:
        err_console.print(f"[red]{result.stderr}[/red]")
        raise ExecutionError


def _check_if_git(path: str):
    cwd_git_file = Path(f"{path}/.git")
    if not cwd_git_file.exists():
        raise IsNotGitRepository


def _find_current(repo_dir: str | None = None):
    result = subprocess.run(
        "git branch --show-current".split(),
        capture_output=True,
        text=True,
        cwd=repo_dir,
    )
    if result.returncode == 0:
        return result.stdout.rstrip()
    else:
        err_console.print(
            f"[red]Failed to fetch current branch with err: {result.stderr}[/red]"
        )
        exit(1)


def _find_main(repo_dir: str | None = None):
    result = _execute(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD", "--short"],
        work_dir=repo_dir,
    )
    return result.stdout.split("/")[1].strip()


def _commit_current(message: str):
    return _execute(["git", "commit", "-am", message])


def sync_current():
    _check_if_git(str(Path.cwd()))
    current_branch = _find_current()
    return _execute(["git", "pull", "origin", current_branch])


def sync_repo(repo_path: str):
    if not Path(repo_path).is_dir():
        raise IsNotDirectory(f"Provided path {repo_path} is not a directory.")
    _check_if_git(repo_path)
    print(f"Synching repo: {repo_path}")
    main_branch = _find_main(repo_path)
    # TODO: fetch output and send to file log
    try:
        checkout = _execute(["git", "checkout", main_branch], work_dir=repo_path)
        print("SUCCESS: checkout to main") if checkout.returncode == 0 else print(
            "ERROR: failed checkout", checkout.stderr
        )
        result = _execute(["git", "pull", "origin", main_branch], work_dir=repo_path)
        if result.returncode != 0:
            raise ExecutionError(result.stderr)
        else:
            print("SUCCESS: Repo was synched")

    except ExecutionError as e:
        print(e)


def send(message):
    _check_if_git(str(Path.cwd()))
    if message:
        _commit_current(message)
    return _execute(["git", "push", "origin", "HEAD"])
