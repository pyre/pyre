#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a document that goes through the editor untouched comes out byte for byte the same
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None
    # the fixture
    text = open("editor.yaml", encoding="utf-8").read()
    # open it
    editor = pyre.config.newYamlEditor(uri="editor.yaml")
    # the rendering is the original
    assert editor.render() == text
    # and the values are reachable by key path
    assert editor.get("crete", "uri") == "earth:crete"
    assert list(editor.get("archives")) == ["qed.archives.earth#crete"]
    assert editor.get("qed.app", "nexus.services.web", "address") == "ip4:0.0.0.0:8005"
    # a path that leads nowhere yields the default
    assert editor.get("crete", "missing") is None
    assert editor.get("crete", "uri", "deeper", default="nope") == "nope"
    # all done
    return editor


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
