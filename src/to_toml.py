#! /usr/bin/env python
"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

To produce a valid TOML file, project.name and project.version are required.

.. py:data:: DEFAULT_PROJECT_NAME
   :type: str
   :value: "whatever"

   A project name. Is ignored. The value type is str.

.. py:data:: DEFAULT_PROJECT_VERSION
   :type: str
   :value: "99.99.99a1.post7.dev6"

      A project version. Is ignored. The value type is str.

.. py:data:: SECTION_NAME
   :type: str
   :value: "config-settings"

   drain-swamp build plugin parameters should to into section ``[tool.config-settings]``

.. py:data:: LINE_SEPERATOR
   :type: str
   :value: "\n"

   TOML file format does not understand Windows line seperator. **Do not use**
   :py:data:`os.linesep`

.. py:data:: ENV_TOML_PATH
   :type: str
   :value: "DS_CONFIG_SETTINGS"

   The environment variable containing the path to the TOML file. drain-swamp
   gets config_settings from the TOML file.

.. py:data:: FILE_APPEND_MODE
   :type: str
   :value: "a"

   open write mode, append to file

.. py:data:: OUTPUT_TOML_PATH
   :type: str
   :value: "ds_config_settings"

   output containing toml path

"""
import json
import os
import sys
from collections.abc import Mapping
from pathlib import Path

DEFAULT_PROJECT_NAME = "whatever"
DEFAULT_PROJECT_VERSION = "99.99.99a1.post7.dev6"
SECTION_NAME = "config-settings"
LINE_SEPERATOR = "\n"
ENV_TOML_PATH = "DS_CONFIG_SETTINGS"
FILE_APPEND_MODE = "a"
OUTPUT_TOML_PATH = "ds_config_settings"


def write_lines_to_streams(lines, streams):
    """Write lines to stream

    :param lines: Lines to write
    :type lines: collections.abc.Sequence[str]
    :param steams: where to write it
    :type streams: collections.abc.Sequence[typing.TextIO[str]]
    """
    eoled_lines = [line + os.linesep for line in lines]
    for stream in streams:
        stream.writelines(eoled_lines)
        stream.flush()


def set_gha_output(name, value):
    """Set an action output using an environment file.

    :param name: Output name. Will be available as ``output.[name]``
    :type name: str
    :param value: Value to set
    :type value: str

    .. seealso::

       `Deprecation Warning <https://hynek.me/til/set-output-deprecation-github-actions/>`_

       `GITHUB_OUTPUT docs <https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter>`_

    """
    outputs_file_path = Path(os.environ["GITHUB_OUTPUT"])
    with outputs_file_path.open(mode=FILE_APPEND_MODE) as outputs_file:
        write_lines_to_streams((f"{name}={value}",), (outputs_file,))


def set_final_result_outputs(path_toml):
    """All the gha output in one place.

    :param path_toml: path to config_settings TOML file
    :type: pathlib.Path
    """
    # Make path available as ``output.ds_config_settings``
    set_gha_output(name=OUTPUT_TOML_PATH, value=str(path_toml))


def parse_as_dict(input_text):
    """Parse given input as JSON or comma-separated list.

    :param input_text:

       JSON str that should contain a mapping of drain-swamp build
       plugin parameters. All plugins receive all parameters

    :type input_text: str
    :returns: mapping of key/value pairs
    :rtype: collections.abc.Mapping[str, str]
    :raises:

       - :py:exc:`json.decoder.JSONDecodeError` -- invalid json

    """
    try:
        d_ret = json.loads(input_text)
    except json.decoder.JSONDecodeError:
        raise

    return d_ret


def main(argv):
    """Script entrypoint

    Produces a config_settings TOML file. Environment variable contains
    the path to the file.

    :raises:

       - :py:exc:`ValueError` -- Required environment variables
         DS_CONFIG_SETTINGS and INPUT_PLUGIN_PARAMETERS are required

       - :py:exc:`json.decoder.JSONDecodeError` -- invalid json

       - :py:exc:`AssertionError` -- INPUT_PLUGIN_PARAMETERS str
         is not loadable or not a Mapping


    """
    str_json = os.environ.get("INPUT_PLUGIN_PARAMETERS", None)
    summary_file_path = Path(os.environ["GITHUB_STEP_SUMMARY"])

    argv_count = len(argv) != 2
    if argv_count or str_json is None:
        with summary_file_path.open(mode=FILE_APPEND_MODE) as summary_file:
            msg_exc = (
                "required environment field INPUT_PLUGIN_PARAMETERS and "
                "temp file path as positional arg"
            )
            write_lines_to_streams(msg_exc, (sys.stderr, summary_file))
            return 1
    else:  # pragma: no cover
        path_toml = Path(argv[1])

    try:
        d_params = parse_as_dict(str_json)
    except Exception:
        with summary_file_path.open(mode=FILE_APPEND_MODE) as summary_file:
            msg_exc = f"parsing json str failed {str_json}"
            write_lines_to_streams(msg_exc, (sys.stderr, summary_file))
            return 2

    # TOML format does not understand ``\r\n``
    toml_contents = (
        f"""[project]{LINE_SEPERATOR}"""
        f"""name = \"{DEFAULT_PROJECT_NAME}"{LINE_SEPERATOR}"""
        f"""version = \"{DEFAULT_PROJECT_VERSION}"{LINE_SEPERATOR}"""
        f"""[tool.{SECTION_NAME}]{LINE_SEPERATOR}"""
    )

    try:
        assert isinstance(d_params, Mapping)
    except AssertionError:
        with summary_file_path.open(mode=FILE_APPEND_MODE) as summary_file:
            msg_err = f"Expected JSON str to parse into a Mapping. got {type(d_params)}"
            write_lines_to_streams(msg_err, (sys.stderr, summary_file))
            return 3

    for k, v in d_params.items():
        # supports str and paths (especially Windows paths)
        # does not support bool or int or float. Pass those as str
        toml_contents += f"""{k!s} = '{v!s}'{LINE_SEPERATOR}"""
    path_toml.write_text(toml_contents)

    # Make path available as ``steps.[step id].outputs.ds_config_settings``
    set_final_result_outputs(path_toml)


if __name__ == "__main__":
    """Process shield."""
    sys.exit(main(sys.argv))
