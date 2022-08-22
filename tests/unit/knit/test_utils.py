from pathlib import Path
from knit.utils import extract_sexp, extract_packages


def test_extract_sexp():
    sample = "(package! doom-themes)"
    assert extract_sexp(sample, 0) == "(package! doom-themes)"

    sample = "(package! doom-themes (package! doom-themes-ext-themes))"
    assert (
        extract_sexp(sample, 0)
        == "(package! doom-themes (package! doom-themes-ext-themes))"
    )


def test_extract_packages():
    sample = """
    (package! doom-themes)
    (package! doom-modeline)
    (package! all-the-icons)
    """

    assert extract_packages(sample) == [
        "(package! doom-themes)",
        "(package! doom-modeline)",
        "(package! all-the-icons)",
    ]
