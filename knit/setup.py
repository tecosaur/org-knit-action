#!/usr/bin/env python3

from subprocess import run
from pathlib import Path

from colour import *

dot_emacs = Path("~/.emacs.d").expanduser()
dot_emacs_doom = Path("~/.emacs.d.doom").expanduser()


def config(url: str):
    if not url.startswith("http"):
        raise ValueError(f"Config url {url} does not appear to actually be a url.")
    print(bblue | "Downloading config")
    if url.endswith(".git"):
        run(["git", "clone", "--depth", "1", url, dot_emacs])
    else:
        run(["mkdir", "-p", dot_emacs])
        run(["wget", url], cwd=dot_emacs)
    if (dot_emacs / "config.org").exists():
        print(blue | "Tangling config.org")
        run(
            [
                "emacs",
                "--batch",
                "--eval",
                "(require 'org)",
                "--eval",
                '(org-babel-tangle-file "~/.emacs.d/config.org")',
            ]
        )
    if not (dot_emacs / "init.el").exists():
        raise FileNotFoundError(f"init.el is required.")
    doom_config = False
    with open(dot_emacs / "init.el", "r") as f:
        if "(doom!" in f.read():
            doom_config = True
        f.close()
    if doom_config:
        print(bmagenta | "Doom detected, syncing")
        dot_doom = Path("~/.config/doom").expanduser()
        run(["mv", dot_emacs, dot_doom])
        run(["mv", dot_emacs_doom, dot_emacs])
        run([dot_emacs / "bin/doom", "sync"])
    print(green | "Emacs config setup complete")


def empty_config():
    run(["mkdir", "-p", dot_emacs])
    with open(dot_emacs / "init.el", "w") as f:
        f.write(";; dummy init file\n")
        f.close()
