def extract_sexp(text: str, index: int) -> str:
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
