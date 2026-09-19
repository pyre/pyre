#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the comments around a list survive the trip from empty to populated and back: the
block that follows an empty list belongs between it and the entry after it, not above the
list, where it would read as a description of the wrong entry
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None
    # a document with an empty list between two commented sections
    text = "\n".join(
        [
            "# the archives",
            "archives:",
            "    - one",
            "",
            "",
            "# the datasets",
            "datasets: []",
            "",
            "",
            "# crew size",
            "tile:",
            "    size: 4",
            "",
        ]
    )
    # load it
    doc = pyre.config.newYamlEditor(text=text)
    # populate the list
    doc.set("datasets", value=["qed.readers.native.flat#flat16"])
    # render
    populated = doc.render()
    # every comment is still ahead of the section it describes
    lines = populated.splitlines()
    assert lines.index("# the datasets") + 1 == lines.index("datasets:")
    assert lines.index("# crew size") + 1 == lines.index("tile:")
    # and the item is in
    assert "    - qed.readers.native.flat#flat16" in lines

    # read the document back, the way the next edit of the file would
    doc = pyre.config.newYamlEditor(text=populated)
    # and empty the list
    doc.set("datasets", value=[])
    # the document is back where it started, to the character
    assert doc.render() == text

    # the same trip by removing the item, which is how a list loses its last entry
    doc = pyre.config.newYamlEditor(text=populated)
    # remove it
    assert doc.remove("datasets", value="qed.readers.native.flat#flat16") is True
    # render
    lines = doc.render().splitlines()
    # the comments are still ahead of their own sections
    assert lines.index("# the datasets") + 1 == lines.index("datasets: []")
    assert lines.index("# crew size") + 1 == lines.index("tile:")

    # all done
    return doc


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
