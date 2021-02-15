#!/usr/bin/env python3

import ast
from typing import Callable
from colour import *

from subprocess import run
from pathlib import Path

work_dir = Path("/github/workspace")


def _type_arr(value, cast_fn):
    value = value.strip()
    if cast_fn == str and '"' not in value and "'" not in value:
        value = value.strip("[]").replace(", ", ",").split(",")
    elif value[0] == "[":
        value = ast.literal_eval(value)
        value = list(map(cast_fn, value))
    else:
        value = [cast_fn(value)]
    return value


def type_arr(cast_fn) -> Callable:
    return lambda value: _type_arr(value, cast_fn)


def _type_or(value, *cast_fns):
    for cast_fn in cast_fns:
        try:
            value = cast_fn(value)
            return value
        except ValueError:
            continue
    raise ValueError(f"Could not cast {value.__repr__()}.")


def type_or(*cast_funs) -> Callable:
    return lambda value: _type_or(value, *cast_funs)


def strict_bool(value):
    if str(value).lower() in ["true", "yes"]:
        return True
    elif str(value).lower() in ["false", "no"]:
        return False
    else:
        raise ValueError(
            f"{value.__repr__()} could not be stictrly cast to True/False."
        )


def _string_or(value, value_func):
    value = _type_or(value, strict_bool, str)
    if isinstance(value, str):
        return value
    else:
        return value_func()


def string_or(value_func):
    return lambda value: _string_or(value, value_func)


def _v_replace(value, cast_fn, old_value, new_value):
    value = cast_fn(value)
    if value == old_value:
        return new_value
    return value


def v_replace(cast_fn, old_value, new_value):
    return lambda value: _v_replace(value, cast_fn, old_value, new_value)


def pp_value(value) -> str:
    if isinstance(value, bool):
        return magenta | str(value)
    elif isinstance(value, int) or isinstance(value, float):
        return yellow | str(value)
    elif isinstance(value, str):
        return green | value.__repr__()
    elif isinstance(value, list):
        return "[" + ", ".join(map(pp_value, value)) + "]"
    else:
        return value.__repr__()


bool_or_str = type_or(strict_bool, str)
str_arr = type_arr(str)
bool_or_str_arr = type_or(strict_bool, str_arr)


def default_branch(directory):
    branch = run(
        ["git", "branch", "--show-current"], capture_output=True, cwd=directory
    )
    return branch.stdout.decode().strip()


class Inputs:
    arg_def = {
        "config": bool_or_str,  # False
        "setup_file": v_replace(bool_or_str, "", False),  # False
        "eval": bool_or_str_arr,  # False
        "tangle": bool_or_str_arr,  # False
        "export": bool_or_str_arr,  # html
        "files": str_arr,  # **.org
        "github_token": bool_or_str,  # False
        "branch": v_replace(bool_or_str, True, default_branch(work_dir)),  # True
        "force_orphan": strict_bool,  # False
        "keep_files": bool_or_str,  # True
        "commit_message": bool_or_str,  # Knit !#!
        "fragile": strict_bool,  # True
    }

    def __init__(self, *args) -> None:
        if len(args) != len(self.arg_def):
            raise ValueError(
                f"Number of arguments passed ({len(args)}) does not match expectation ({len(self.arg_def)})."
            )
        parsed_args = {}
        args = list(args)
        for arg_name, caster in self.arg_def.items():
            arg = args.pop(0)
            try:
                parsed_args[arg_name] = caster(arg)
            except ValueError as err:
                print(
                    (bred | "Invalid parameter value!")
                    + f" {pp_value(arg)} could not be cast as "
                    + (
                        yellow
                        | (
                            [name for name in globals() if globals()[name] is caster]
                            + ["?"]
                        )[0]
                    )
                    + "\n"
                    + (red | str(err))
                )
            self.args = parsed_args

    def pretty_print(self):
        return "\n".join(
            [
                (bgrey | f"{key: >16}") + " " + pp_value(value)
                for key, value in self.args.items()
            ]
        )

    def __getattr__(self, key):
        return self.args[key]

    def __repr__(self):
        return str(self.args)
