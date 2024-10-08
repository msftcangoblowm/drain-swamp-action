.. this could be appended to README.rst

Changelog
=========

..

   Feature request
   .................

   - add input is_arch

   Known regressions
   ..................

   Commit items for NEXT VERSION
   ..............................

   - ci: add codeql-analysis
   - ci: add dependency-review and dependabot
   - refactor(show-me): assert env.DS_CONFIG_SETTINGS into one step
   - chore: bump actions/checkout
   - fix(show-me): remove input fetch_tags
   - fix(action): remove input fetch_tags
   - docs(README): remove mention of input fetch_tags
   - fix(action): specify this gha repo and branch v1
   - fix(show-me): assert env.DS_CONFIG_SETTINGS and show file contents
   - fix: remove output ds_config_settings. Prefer env.DS_CONFIG_SETTINGS
   - fix: download artifact then set DS_CONFIG_SETTINGS
   - fix: improve showing state before upload and after download
   - ci(show-me): download artifact check contents
   - fix(action): fix bash boolean evaluation. case not if
   - fix(gh_joinpath): argparse.parse_known_args returns a tuple
   - fix(gh_joinpath): parse --dir type pathlib.PurePath
   - fix: archive id missing python-version
   - fix(gh_joinpath): add option --dir
   - fix: on Windows try env.GITHUB_WORKSPACE
   - fix(action): consolidate output onto one id
   - fix(gh_joinpath): on Windows outside repository path use Path.as_posix
   - fix(gh_joinpath): use GITHUB_ACTION_PATH not GITHUB_WORKSPACE
   - ci(show-me): replace input cache --> fetch_tags
   - fix(action): single quote Windows path
   - fix(action): specify path to gh_joinpath

.. scriv-start-here

.. _changes_1-0-0:

Version 1.0.0 — 2024-09-15
--------------------------

- feat: OS independent
- feat: add input fetch_tags
- feat: leverage GITHUB_ENV to create environment variables
- feat(gh_joinpath): OS independent joinpath
- fix: remove input cache
- fix: remove main.sh
- fix(action): run python scripts without main.sh
- fix: move python setup step up top
- fix(gh_joinpath): line seperator between lines
- fix: steps must have unique id
- fix: env variable path seperator split steps by matrix.os
- fix: disable cache pip. Does not work and causes runner to fail
- fix(action): try without upload / download artifact
- fix(action): set python scripts executable
- fix(action): typo steps.outputs not steps.outout
- fix(action): try startsWith rather than contains
- fix: requirements.txt is required
- fix(action): specify shell bash
- docs: remove mention of fromJSON

.. _changes_0-0-1:

Version 0.0.1 — 2024-09-14
--------------------------

- feat: add action.yml main.sh src/to_toml.py
- docs: add LICENSE aGPLv3+ README.rst NOTICE.txt CHANGES.rst
- ci: add workflow show-me.yml
- chore: add boilerplate .gitignore

.. scriv-end-here
