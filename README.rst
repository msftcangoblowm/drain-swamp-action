.. _drain-swamp-action:

drain-swamp-action
===================

Make config settings available to Python build backend

This technique is a workaround to an issue affecting setuptools. Any build backend
is welcome to use this workaround / github action.

``drain-swamp``, a build backend with build plugins for generated files,
uses this technique. So could your build backend.

:code:`python -m build` executes build backends within a subprocess. And
does not pass thru the config_settings.

To customize the build process, config settings are absolutely needed.

Definitions
------------

- ``DS_CONFIG_SETTINGS``

Environment variable with absolute path to a valid TOML file

- a valid TOML file

Holds the config settings. Values are all str. Path values need
single quotes, not double quotes.

- custom build backends

Python build backend packages also need to build their package.

Your package most likely is not a build backend package.

**to be consistent**

Eventhough ``config_settings`` is passed into the custom build
backend Python script, all packages should use the same
interface, ``drain-swamp-action``.

Workflow
---------

The build backend should:

- check for ``DS_CONFIG_SETTINGS`` which contains absolute TOML file path
  e.g. ``'/[tmp folder]/setuptools-build.toml'``
- read the TOML file
- parse (``config_settings``) into a mapping
- use the ``config_settings`` mapping to customize the build process

tl;dr; skip to github-workflow_

.. _custom-build-backends:

Setuptools -- custom build backends
------------------------------------

Sending config_settings to a setuptools **custom** build backend. This
applies only to those who are a build backend author.

.. code-block:: shell

   python -m build -C--set-lock="1" -C--kind="0.0.1"

The drain-swamp build plugins then have access to both:

.. code-block:: text

   --set-lock="1" --kind="0.0.1"

In an ideal world, the conversation would end here. This technique
would work for both custom build backends and when using a build backend.

This is the hottest topic in setuptools issues. Below is the suggested
interm solution, before the community can reach a consensus (aka a PEP).

config_settings TOML file format
---------------------------------

.. csv-table:: Config settings
   :header: property, desc
   :widths: auto

   "project.name", "required and ignored"
   "project.version", "required and ignored"
   "tool.config-settings.kind", "semantic version str or current or tag"
   "tool.config-settings.set-lock", "'1' or '0'. dependency lock on and off respectively"
   "tool.config-settings.snip-co", "| Only if pyproject.toml contains more than one snippet.
   | Need the snippet code for the snippet
   | containing dependencies and optional-dependencies"
   "tool.config-settings.parent-dir", "Only used during testing. Sets the tmp/ folder"

The ``[tool.config-settings]`` section contains whatever key/value pairs
the build backend needs to customize the build process.

These are the config settings used by ``drain-swamp``

Technique -- bash implementation
---------------------------------

.. code-block:: text

   export DS_CONFIG_SETTINGS="/tmp/setuptools-build.toml"

   cat <<-EOF > "$DS_CONFIG_SETTINGS"
   [project]
   name = "whatever"
   version = "99.99.99a1.dev6"
   [tool.config-settings]
   kind="1.0.0"
   set-lock="0"
   EOF

   python -m build

``drain-swamp`` has build plugins. These input parameters are received
by all build plugins. So the plugin should use only the needed key/value pairs.
The plugin should ignore all other key/value pairs.

Add key/value pairs to ``[tool.config-settings]`` section.

To verify this TOML file is valid

.. code-block:: shell

   python -m pip install --upgrade validate-pyproject
   validate-pyproject $DS_CONFIG_SETTINGS

.. _github-workflow:

Github Workflow
----------------

Github workflows can use this drain-swamp-action to simplify the process.

``config_settings`` are passed in as a JSON str.

.. code-block:: text

   - name: "Build Plugin parameters"
     uses: 'msftcangoblowm/drain-swamp-action@v1'
     with:
        plugin_parameters: '{"set-lock": "1", "kind": "current"}'
        checkout: true
        python_version: '3.10'

Can easily and intuitively add more build parameters to the JSON str.

After this step, execute :code:`python -m build`. This your github
workflow should do.

Usually implemented as bash or tox.

**Resist the urge**

This is wrapping repo checkout and python setup. Your github workflow
might already do this, but why? It's already done for you.

JSON tools
"""""""""""

Available within github workflows and github actions

jq_, toJSON_, fromJSON_, and join_

.. _jq: https://stedolan.github.io/jq/
.. _fromJSON: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#fromjson
.. _toJSON: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#tojson
.. _join: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#join

.. _drain-swamp-action-inputs:

IO
---

.. csv-table::
   :header: inputs, desc
   :widths: 120, 350

   "plugin_parameters", "a JSON str holding key/value pairs to deliver as config_settings thru the subprocess barrier"
   "toml_file_name", "| file name to store config_settings in TOML format.
   | Default \'setuptools-build.toml\'"
   "checkout", "| ``true`` to checkout repo. Let us checkout the repo, one less thing to do.
   | Default true"
   "python_version", "| Version of python to use.
   | Default \'3.10\'"

.. csv-table::
   :header: outputs, desc
   :widths: 120, 350

   "ds_config_settings", "| Absolute path to the toml file. Set this into environment variable, DS_CONFIG_SETTINGS.
   | Path to the toml file within the runners temp folder"

Example usage, although ``env.DS_CONFIG_SETTINGS`` should already exist
along with the TOML file

.. code-block:: text

   id: steps-id-goes-here
   env:
     DS_CONFIG_SETTINGS: ${{ steps.steps-id-goes-here.outputs.ds_config_settings }}

**Not shown**

.. code-block:: text

   On windows, value (an absolute path) needs single quotes.

   In bash, use ``case in esac`` to handle windows and not windows cases.

   These produce boolean, so don't use ``if; then else fi``

   ${{ ! startsWith(matrix.os, 'windows') }}
   startsWith(matrix.os, 'windows')

.. _drain-swamp-action-examples:

Examples
---------

.. _github-workflow-example-multiple-snippets:

Complete
"""""""""

Basic example

.. code-block:: text

   - id: prepare-config-settings
     name: "Build Plugin parameters"
     uses: 'msftcangoblowm/drain-swamp-action@v1'
     with:
        plugin_parameters: '{"set-lock": "1", "kind": "current"}'
        checkout: true
        python_version: '3.10'

   - name: "What did we get?"
     run: |
       ls -alR

   # If using tox, install requirements for tox and tox-gh
   - name: "Build package"
     env:
       DS_CONFIG_SETTINGS: ${{ steps.prepare-config-settings.outputs.ds_config_settings }}
     run: |
       python -m build

.. note: Windows paths

   On Windows, single quotes preserves (the backslashes in) the path. Add single quotes
   around ``env.DS_CONFIG_SETTINGS``'s value

Multiple snippets
""""""""""""""""""

Lets say ``pyproject.toml`` has multiple snippets. Cuz snippets are
awesome and more is better!

Only in this case, specify the snip-co parameter.

.. code-block:: text

   - name: "Build Plugin parameters"
     uses: 'msftcangoblowm/drain-swamp-action@v1'
     with:
        plugin_parameters: '{"set-lock": "1", "kind": "current", "snip-co": "little_shop_of_horrors_shrine_candles"}'

Checks out repo and setup python py310 without the cache.

If there is only one snippet, ``snip-co`` is inferred; so unnecessary.

If a ``snip-co`` is needed, don't provide an incorrect ``snip-co``. That
would result in an exception.

The refresh links plugin expects the snippet to contain: dependencies and optional-dependencies.

For the love of cringe and cosplay, the snippet codes are movie references with
cringe scenes. Something in a scene or what's cringe about the scene are good
candidates for a ``snip-co``.
