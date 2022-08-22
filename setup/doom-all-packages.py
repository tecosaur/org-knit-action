#!/usr/bin/env python3

from pathlib import Path

from knit.utils import extract_packages

dot_emacs = Path("~/.emacs.d").expanduser()
doom_package_files = (dot_emacs / "modules").rglob("**/packages.el")

doom_packages = []

for package_file in doom_package_files:
    with open(package_file) as f:
        content = f.read()
        doom_packages.extend(extract_packages(content))

print(f";; {len(doom_packages)} packages found in modules")
print("\n".join(doom_packages))
