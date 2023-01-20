#!/usr/bin/env python3

"""
Extract git paths beyond renames and moves.

Usage:
  git-relevant-history [options] --subdir=<subdir> --outfile=<filename>

Files starting with <subdir>, relative to the current working directory, will have their relevant historical paths written to the file <outfile>.
This file can be given as input to git-filer-repo with argument --paths-from-file.


Options:
  -h --help            show this help message and exit
  -v --verbose         print status messages

"""
import logging
import pathlib
import subprocess
import typing

from docopt import docopt

log_format = "%(message)s"
logging.basicConfig(format=log_format, level=logging.DEBUG)

logger = logging.root

def build_git_filter_path_spec(str_subdir: str) -> typing.List[str]:
    all_filter_paths = []
    all_rename_statements = []

    for strpath in pathlib.Path(str_subdir).rglob('*'):
        path = pathlib.Path(strpath)

        if path.is_file():

            logger.debug(f"Including {path} with history")

            unique_paths_of_current_file = {str(path)}

            git_args = ["git",
                        "log",
                        "--pretty=format:",
                        "--name-only",
                        "--follow",
                        "--",
                        str(path)]
            logger.debug(f"Calling {' '.join(git_args)}")
            try:
                gitlog = subprocess.check_output(git_args,
                                                 universal_newlines=True)

                for line in gitlog.splitlines(keepends=False):
                    if len(line) > 0:
                        unique_paths_of_current_file.add(line.strip())

                if logger.isEnabledFor(logging.DEBUG):
                    this_file_paths_newlines = '\n\t'.join(unique_paths_of_current_file)
                    logger.debug(f"\t{this_file_paths_newlines}\n")

                all_filter_paths.extend(unique_paths_of_current_file)

            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to get hystorical names of {path}, stdout: {e.output}, stderr: {e.stderr}")
                logger.warning(f"Failed command: {' '.join(git_args)}")

    if logger.isEnabledFor(logging.DEBUG):
        all_rename_statements_newlines = '\n\t'.join(all_rename_statements)
        logger.debug(f"All renames:\n\t{all_rename_statements_newlines}")
    return all_filter_paths


def main():
    arguments = docopt(__doc__)
    if arguments["--verbose"]:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    subdir = arguments["--subdir"]
    if not subdir.endswith('/'):
        subdir = subdir + '/'

    subdir = pathlib.Path(subdir)
    if not subdir.is_dir():
        logger.critical(f"--subdir {subdir} is not a directory")
        raise SystemExit(-1)

    outfile = arguments["--outfile"]
    logger.info(f"Will write relevant history of { subdir } to file {outfile}")

    filenameset = build_git_filter_path_spec(subdir)
    with open(outfile, "w") as outfile:
        for line in filenameset:
            outfile.write(line)
            outfile.write('\n')

        logger.debug(f"Stored filter repo specs in {outfile}")


if __name__ == '__main__':
    main()
