from knit.utils import extract_sexp


def test_extract_sexp():
    sample = "(package! doom-themes)"
    assert extract_sexp(sample, 0) == "(package! doom-themes)"

    sample = "(package! doom-themes (package! doom-themes-ext-themes))"
    assert (
        extract_sexp(sample, 0)
        == "(package! doom-themes (package! doom-themes-ext-themes))"
    )
