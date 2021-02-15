#!/usr/bin/env python3

from subprocess import run
from os import environ
from pathlib import Path

from inputs import Inputs
from colour import *


def git_result(work_dir, *args):
    r = run(["git", *args], cwd=work_dir, capture_output=True)
    return r.stdout.decode().strip()


def remote_from_token(I: Inputs):
    # TODO add checks, i.e. is branch prohibited? is repo external?
    return f"https://x-access-token:{I.github_token}@github.com/{environ['GITHUB_REPOSITORY']}.git"


def push(work_dir: Path, I: Inputs):
    def git(*args):
        return run(["git", *args], cwd=work_dir)

    print(blue | f"Configure repository to push to {I.branch}")

    if I.keep_files == True:
        git("remote", "rm", "origin")

    if I.force_orphan:
        run(["rm", "-rf", work_dir.absolute() / ".git"])
        git("init")

    if git("show-ref", "-q", "--heads").returncode != 0:
        git("branch", I.branch)

    git("checkout", I.branch)

    print(blue | "Add remote, and stage files")

    git("remote", "add", "origin", remote_from_token(I))

    git("add", "--all")

    git("config", "user.name", I.name)
    git("config", "user.email", I.email)

    message = I.commit_message.replace("!#!", environ["GITHUB_SHA"])
    git("commit", "-m", message)

    print(f'Commited: "{message}"')

    if I.force_orphan:
        git("push", "origin", "--force", I.branch)
    else:
        git("push", "origin", I.branch)

    print(green | f"Pushed.")
