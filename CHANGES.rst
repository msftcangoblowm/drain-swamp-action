.. this could be appended to README.rst

Changelog
=========

..

   Feature request
   .................

   Known regressions
   ..................

   Commit items for NEXT VERSION
   ..............................

   - fix(main): execute py script rely on hashbang
   - fix: move python setup step up top
   - fix(gh_joinpath): line seperator between lines
   - feat: leverage GITHUB_ENV to create environment variables
   - fix(main): python get path via environment variable
   - fix(main): fix path to to_toml.py
   - fix: steps must have unique id
   - fix: env variable path seperator split steps by matrix.os
   - fix: OS independent joinpath
   - fix(action): cache pip maybe needs cache-dependency-path
   - fix(action): try without upload / download artifact
   - fix(action): archive name append matrix.os and version
   - fix(action): upload and download archive name must be same
   - fix(action): typo steps.outputs not steps.outout
   - fix(to_toml): set executable
   - fix(action): set script executable
   - fix(action): if run add indention
   - fix(action): try startsWith rather than contains
   - fix(action): set script permissions executable
   - fix: mkdir prevent fail
   - fix: requirements.txt is required
   - fix(action): specify shell bash
   - fix(show-me): steps not step
   - docs: remove mention of fromJSON

.. scriv-start-here

.. _changes_0-0-1:

Version 0.0.1 — 2024-09-14
--------------------------

- feat: add action.yml main.sh src/to_toml.py
- docs: add LICENSE aGPLv3+ README.rst NOTICE.txt CHANGES.rst
- ci: add workflow show-me.yml
- chore: add boilerplate .gitignore

.. scriv-end-here
