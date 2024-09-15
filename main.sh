#!/bin/bash

# set -x
set -e

echo ::group:: Initialize various paths

repo_dir=$GITHUB_WORKSPACE/$INPUT_REPOSITORY_PATH
# doc_dir=$repo_dir/$INPUT_DOCUMENTATION_PATH
# https://stackoverflow.com/a/4774063/4799273
# action_dir=$PYTHONPATH
site_packages_dir=$(python -c 'import site; print(site.getsitepackages()[0])')

# echo Action: $action_dir
echo Workspace: $GITHUB_WORKSPACE
echo Repository: $repo_dir
# echo Documentation: $doc_dir
echo Python site-packages directory: $site_packages_dir
echo to_toml.py path: $TO_TOML

echo ::endgroup::

#
# Use runners tmp directory
#

# echo ::group:: Creating tmp directory
# build_dir=/tmp
# mkdir -p $build_dir ||:
# echo Temp directory \"$build_dir\" is created
# echo ::endgroup::

echo ::group:: config_settings write into TOML file

# execute python script
# Inputs -- environment variables: DS_CONFIG_SETTINGS, INPUT_PLUGIN_PARAMETERS, GITHUB_STEP_SUMMARY
# Outputs --
#    path_toml_file
#    writes a toml file to /tmp/$DS_CONFIG_SETTINGS
#
# Example JSON str
# '{ "set-lock": "1", "kind": "0.0.1" }'
# to_toml=$(python -c 'import os; import platform; from pathlib import PurePosixPath, PureWindowsPath; import sys; cls = PureWindowsPath if platform.system().lower() == "windows" else PurePosixPath; path_f = cls(os.environ.get("GITHUB_WORKSPACE")).joinpath("src", "to_toml.py"); sys.stdout.write(str(path_f))')
$TO_TOML
exit_code=$?
if [[ $exit_code -ne 0 ]]; then
    echo "drain-swamp-action exit code: $exit_code"
fi

echo ::endgroup::

exit $exit_code
