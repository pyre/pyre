#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the editor finds entries the way the configuration loader scopes them: by the
dotted name a setting is known by, across keys that spell several levels of it and keys that
carry a family, and by the line a locator points at
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None
    # open the fixture
    doc = pyre.config.newYamlEditor(uri="editor.yaml")
    # a plain nested setting
    assert doc.find("crete.polygon") == ("crete", "polygon")
    # a section
    assert doc.find("crete") == ("crete",)
    # a key that spells two levels of the name
    assert doc.find("qed.app.shell") == ("qed.app", "shell")
    # nested below one that spells three
    assert doc.find("qed.app.nexus.services.web.address") == (
        "qed.app",
        "nexus.services.web",
        "address",
    )
    # a name spelled partly by a key with a family
    doc.set("qed.archives.earth#crete", "count", value=3)
    assert doc.find("crete.count") == ("qed.archives.earth#crete", "count")
    # names the document does not configure
    assert doc.find("crete.missing") is None
    assert doc.find("nowhere") is None
    # a name that a key spells more of than there is
    assert doc.find("qed") is None
    # by line: the lines of the fixture, counting from one
    lines = open("editor.yaml", encoding="utf-8").read().splitlines()
    # the line of the collection
    line = 1 + next(i for i, text in enumerate(lines) if text.strip().startswith("collection:"))
    assert doc.locate(line=line) == ("crete", "collection")
    # the line of a nested key
    line = 1 + next(i for i, text in enumerate(lines) if text.strip().startswith("address:"))
    assert doc.locate(line=line) == ("qed.app", "nexus.services.web", "address")
    # a line with no key
    assert doc.locate(line=1) is None
    # all done
    return doc


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
