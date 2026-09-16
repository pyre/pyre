#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a document saved by the editor reads back the same, and that a document opened
at a location that does not exist starts out empty and creates the file when saved
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None
    # the scratch product
    product = "yaml_editor_save.yaml"
    # a defensive guard against a stale product
    import os

    if os.path.exists(product):
        os.remove(product)
    # open a document that does not exist
    editor = pyre.config.newYamlEditor(uri=product)
    # it is empty
    assert editor.get("anything") is None
    # fill it
    editor.set("local", "uri", value="file:/tmp/data")
    editor.append("archives", value="qed.archives.local#local")
    # save it
    editor.save()
    # the file is there
    assert os.path.exists(product)
    # and nothing else was left behind
    assert not os.path.exists(f".{product}.editing")
    # read it back
    again = pyre.config.newYamlEditor(uri=product)
    # the contents survived
    assert again.get("local", "uri") == "file:/tmp/data"
    assert list(again.get("archives")) == ["qed.archives.local#local"]
    # remove the archive
    assert again.remove("archives", value="qed.archives.local#local")
    # and the section
    assert again.delete("local")
    # save again
    again.save()
    # and check that the document is now empty
    assert pyre.config.newYamlEditor(uri=product).get("archives") == []
    # all done
    return again


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
