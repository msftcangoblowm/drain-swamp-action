#! /usr/bin/env python
"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

Writes path pieces to GITHUB_ENV file. The writen key/value pairs will be
available as environment variables **in other steps**, not the step that
calls this script

Test script

.. code-block:: shell

   GITHUB_ENV=log.txt GITHUB_WORKSPACE=src python gh_joinpath.py --name="BOB" "src" "to_toml.py"
   cat log.txt
   rm log.txt

Expected contents

.. code-block::

    BOB = src / src / to_toml.py

The 1st ``src/`` is supposed to be the GITHUB_WORKSPACE absolute path

.. py:data:: DEFAULT_ENV_VAR_NAME
   :type: str
   :value: "ENV_VAR"

   Fallback environment variable name

"""
import argparse
import os
import platform
import sys
from pathlib import PurePosixPath, PureWindowsPath

DEFAULT_ENV_VAR_NAME = "ENV_VAR"


def _parser():
    """script arg parser.

    :returns: CLI parser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path_piece",
        nargs="+",
    )
    parser.add_argument(
        "--name",
        nargs="?",
        const=DEFAULT_ENV_VAR_NAME,
        default=DEFAULT_ENV_VAR_NAME,
    )
    return parser


def main():
    """Write key/value pair to GITHUB_ENV file.

    Inputs

    ``--dir`` -- :code:`git config safe.directory` fallback is GITHUB_ACTION_PATH

    ``--name`` -- output environment variable name

    ``path pieces`` -- path components that will be joined

    Outputs

    ``env.[args.name]`` -- Environment variable that will contain the path

    """
    PATH_CLS = (
        PureWindowsPath if platform.system().lower() == "windows" else PurePosixPath
    )
    # GH_WORKSPACE = os.environ.get("GITHUB_WORKSPACE")

    parser = _parser()
    args = parser.parse_args()

    env_var_name = args.name
    path_pieces = args.path_piece
    if hasattr(args, "dir") and len(args.dir) != 0:
        # Get safe directory folder, ``git config safe.directory``
        dir_path = args.dir
    else:
        # Linux and MacOS ok. Windows ng
        dir_path = os.environ.get("GITHUB_ACTION_PATH")
    path_f = PATH_CLS(dir_path)

    # Get the path of the runner file
    for piece_path in path_pieces:
        path_f = path_f.joinpath(piece_path)

    # write to the file
    env_file = os.environ.get("GITHUB_ENV")
    with open(env_file, "a") as env_file:
        env_file.write(f"{env_var_name!s}={path_f.as_posix()}{os.linesep}")


if __name__ == "__main__":
    """Process shield."""
    sys.exit(main())
