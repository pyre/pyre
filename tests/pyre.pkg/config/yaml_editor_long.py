#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a long value is written on one line: the backend would fold a plain scalar past
its line width, and a folded uri with a colon in it reads back as a key
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None
    # a uri well past the width the backend folds at
    uri = "file:/var/folders/z2/krm6rt2d0fn_h5v036n0tg980000gn/T/qed-archive-abcdefghijklmnop/nested/deeper"
    # an empty document
    doc = pyre.config.newYamlEditor(text="")
    # with the uri nested a few levels down, and in a list
    doc.set("archive", "uri", value=uri)
    doc.set("archive", "expanded", value=[uri, uri + "/more"])
    # render
    text = doc.render()
    # the uri sits on one line, twice
    assert text.count(uri) == 3
    assert all(uri in line for line in text.splitlines() if "file:" in line)
    # and the document reads back whole, through the editor
    again = pyre.config.newYamlEditor(text=text)
    assert again.get("archive", "uri") == uri
    assert list(again.get("archive", "expanded")) == [uri, uri + "/more"]
    # and through the loader pyre uses
    import yaml

    loaded = yaml.safe_load(text)
    assert loaded["archive"]["uri"] == uri
    # all done
    return doc


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
