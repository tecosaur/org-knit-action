#!/usr/bin/env python3

from pathlib import Path
import re

dot_emacs = Path("~/.emacs.d").expanduser()

doom_modules = dot_emacs / "modules"

doom_package_files = doom_modules.rglob("**/packages.el")


def sexp_extract(position, text):
    if text[position] != "(":
        raise ValueError('s-expression did not start with "("')
    stack = 0
    point = position
    while point < len(text):
        if text[point] == "(":
            stack += 1
        elif text[point] == ")":
            stack -= 1
            if stack == 0:
                return text[position : point + 1]
        point += 1
    raise ValueError(f"Text did not terminate s-expression started at {position}")


def extract_packages(package_file: Path):
    package_content = open(package_file, "r").read()
    return [
        sexp_extract(m.start(), package_content)
        for m in re.finditer(r"\(package!", package_content)
    ]


doom_packages = []

for package_file in doom_package_files:
    doom_packages.extend(extract_packages(package_file))

print(f";; {len(doom_packages)} packages found in modules")

print("\n".join(doom_packages))
