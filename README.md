# git-relevant-history

Extract software component from git repo into a new repo, taking complete relevant history with it.

## Background

When software evolves, it is typical for a stable, established software component to be moved out of a git repository to facilitate more comprehensive reuse. One of the pain points of such a move would be losing git history, breaking the possibility of using `git blame` or `git log` to understand what led to the current design.

Historically git filter-branch was used for such extracting, and https://github.com/newren/git-filter-repo is a much faster alternative recommended by git now. Both tools work on a static list of path patterns to preserve, so file renames in the past are usually "cut point."

This tool also starts with "what is subcomponent in the current repo to extract?" but then analyzes the history of renames for any existing file. Such a list is used to create a list of patterns for `git filter-repo` so that effectively the old repo/component becomes standalone repo with a full history of every file, as long as git --follow catches the rename.

So from the extracted component perspective, the only history "lost" is one that would require manual analysis of commits to find file merging/splitting.


## Help
Usage documentation for the tool is available via cmdline:

git-relevant-history --help:

```
Extract git paths beyond renames and moves.
Usage:
  git-relevant-history [options] --subdir=<subdir> --outfile=<filename>
Files starting with <subdir>, relative to the current working directory, will have their relevant historical paths written to the file <outfile>.
This file can be given as input to git-filer-repo with argument --paths-from-file.
Options:
  -h --help            show this help message and exit
  -v --verbose         print status messages

```
