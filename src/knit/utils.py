import re
from typing import List


def extract_sexp(text: str, index: int) -> str:
    """Extract the s-expression that starts at a given index."""
    if text[index] != "(":
        raise ValueError('S-expression did not start with "("')

    stack = 0
    for c in range(index, len(text)):
        if text[c] == "(":
            stack += 1
        elif text[c] == ")":
            stack -= 1
            if stack == 0:
                return text[index : c + 1]
    raise ValueError(f"Text did not terminate s-expression started at {index}")


def extract_packages(content: str) -> List[str]:
    """Extract all the packages from a elisp file."""
    return [
        extract_sexp(content, m.start())
        for m in re.finditer(r"\(package!", content)
    ]
