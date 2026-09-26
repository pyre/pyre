<!--
-*- markdown -*-
-*- coding: utf-8 -*-

michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2026 all rights reserved
-->

# Contributing

Thank you for your interest in pyre. The conventions every contribution follows, from file
layout and comments to commits and pull request descriptions, are in [AGENTS.md](AGENTS.md);
they apply to people and coding agents alike.

The mechanical conventions are checked on every pull request. To run the same checks before
pushing:

```
pip install -r etc/ci/conventions/requirements.txt
python3 etc/ci/conventions/check.py --base origin/main
```

A word the spell checker does not know is either a typo, to be fixed, or a real word, to be
added to `etc/ci/conventions/codespell-words.txt`; a single line that is right as it is goes in
`etc/ci/conventions/codespell-lines.txt`. Both lists are reviewed like any other change.


<!-- end of file -->
