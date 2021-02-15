#!/usr/bin/env -S python3 -u

import inputs, setup, push, knit
from colour import *

import concurrent.futures
from pathlib import Path
import sys

from fnmatch import fnmatch
from shutil import copy, copytree

exit_code = 0
github_work_dir = Path("/github/workspace")

print(cyan | "Starting org-knit")

I = inputs.Inputs(*sys.argv[1:])

I.args["name"] = push.git_result(github_work_dir, "log", "-1", "--format=%an", "HEAD")
I.args["email"] = push.git_result(github_work_dir, "log", "-1", "--format=%ae", "HEAD")

print("::group::configuration")
print(I.pretty_print())
print("::endgroup::")

if I.config:
    print("::group::setup emacs config")
    setup.config(I.config)
    print("::endgroup::")
else:
    setup.empty_config()

if I.commit_message and I.branch and not I.github_token:
    print(red | "GitHub Token missing, will not be able to create commit.")
    exit(1)


work_dir = Path("/tmp/workspace")

if I.keep_files == True:
    copytree(github_work_dir, work_dir)
else:
    work_dir.mkdir()
    files = []
    for glob in I.files:
        files.extend(list(github_work_dir.glob(glob)))
    if I.keep_files != False:
        for glob in I.keep_files:
            files.extend(list(github_work_dir.glob(glob)))
    for f in files:
        copy(f, work_dir / f.relative_to(github_work_dir))


print("::group::export and tangle")

files = []
for glob in I.files:
    files.extend(list(work_dir.glob(glob)))

if len(files) == 0:
    print(yellow | "No files to process")
    print("::endgroup::")
    exit()

print(
    (bblue | str(len(files)))
    + (blue | f" file{'s' if len(files) > 1 else ''} to process: ")
    + ", ".join(map(lambda f: (bblue | str(f.relative_to(work_dir))), files))
)

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_result = {}
    if I.export:
        future_to_result.update(
            {
                executor.submit(
                    knit.export,
                    f,
                    form,
                    I,
                ): ("exported", f, form)
                for f in files
                for form in I.export
            }
        )
    if I.tangle:
        future_to_result.update(
            {
                executor.submit(knit.tangle, f, I): ("tangled", f, None)
                for f in files
                if I.tangle == True or any([fnmatch(f, glob) for glob in I.tangle])
            }
        )

    for future in concurrent.futures.as_completed(future_to_result):
        action, f, form = future_to_result[future]
        try:
            data = future.result()
        except Exception as exc:
            print(
                (red | " ✗ ")
                + (bold | str(f.relative_to(work_dir)))
                + " was not "
                + action
                + (" to " + (cyan | form) if form else "")
                + "\n   "
                + "\n   ".join([red | line for line in str(exc).split("\n")])
            )
            if I.fragile:
                exit_code = 1
        else:
            print(
                (green | " ✓ ")
                + (bold | str(f.relative_to(work_dir)))
                + " "
                + action
                + (" to " + (cyan | form) if form else "")
                + " sucessfully"
            )
            if isinstance(data, str) and data != "":
                print(
                    "   " + "\n   ".join([yellow | line for line in data.split("\n")])
                )

print("::endgroup::")

if I.commit_message and I.branch:
    print("::group::pushing")
    push.push(work_dir, I)
    print("::endgroup::")

if exit_code == 0:
    print(bgreen | "Completed")
else:
    print(bred | "Failed")

exit(exit_code)
