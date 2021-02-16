
# Table of Contents

1.  [Parameters](#orgafbbd40)
    1.  [Exporting](#orgea4d951)
    2.  [Publishing](#orgdcd3973)

Let someone else take care of keeping up to date tangled/woven versions of your
Org files for public consumption.

    - name: Export org files
      uses: tecosaur/org-knit-action
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}


<a id="orgafbbd40"></a>

# Parameters

-   **`parameter` (`default`):** description


<a id="orgea4d951"></a>

## Exporting

-   **`config` (`false`):** Path to either an `init.el` file, or a repository url for `~/.emacs.d`.
    This also recognises Doom configuration repositories (`~/.config/doom`).
-   **`setup_file` (`false`):** URL for a `#+setupfile` to use in all Org files.
-   **`eval` (`false`):** Whether to evaluate code in Org files. Also accepts a list of
    globs specifying which Org files should be evaluated.
-   **`tangle` (`false`):** Whether to run `org-tangle` for each Org file. Also accepts a list of
    globs specifying which Org files should be tangled.
-   **`export` (`html`):** Comma separated list of formats to export to.
-   **`files` (`**/*.org`):** List of org file globs to act on.


<a id="orgdcd3973"></a>

## Publishing

-   **`github_token`:** The `GITHUB_TOKEN` secret. Required to push any result.
-   **`branch` (default branch):** The branch to push files to
-   **`force_orphan` (`false`):** Force-push the created commit as the only commit on
    the branch.
-   **`keep_files` (`true`):** Whether to include non-org-related files. Also accepts a
    list of globs.
-   **`commit_message` (`Knit: !#!`):** Commit message to use. `!#!` is replaced with the
    triggering commit hash.
-   **`fragile` (`true`):** Fail the action if any export/tangle steps fail.

