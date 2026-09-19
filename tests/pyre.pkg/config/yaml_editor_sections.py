#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a new top level section is set apart from the one before it the way the document
sets its sections apart, even when the document does not end with the empty lines or the
comment block that would otherwise supply the separation
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None

    # the section to add
    def extend(text):
        # load the document
        doc = pyre.config.newYamlEditor(text=text)
        # add a section
        doc.set("new", "uri", value="file:somewhere")
        # and hand off the text
        return doc.render()

    # a document whose sections are one empty line apart, and which ends without one
    assert extend("a:\n    x: 1\n\nb:\n    y: 2\n") == (
        "a:\n    x: 1\n\nb:\n    y: 2\n\nnew:\n    uri: file:somewhere\n"
    )
    # a document whose sections are two empty lines apart
    assert extend("a:\n    x: 1\n\n\nb:\n    y: 2\n") == (
        "a:\n    x: 1\n\n\nb:\n    y: 2\n\n\nnew:\n    uri: file:somewhere\n"
    )
    # the comments that lead a section do not count as separation, the empty lines above them do
    assert extend("a:\n    x: 1\n\n\n# about b\nb:\n    y: 2\n") == (
        "a:\n    x: 1\n\n\n# about b\nb:\n    y: 2\n\n\nnew:\n    uri: file:somewhere\n"
    )
    # a document that runs its sections together gets what it asked for
    assert extend("a:\n    x: 1\nb:\n    y: 2\n") == (
        "a:\n    x: 1\nb:\n    y: 2\nnew:\n    uri: file:somewhere\n"
    )
    # a document with a single section has no habit to follow, so it gets one empty line
    assert extend("a:\n    x: 1\n") == "a:\n    x: 1\n\nnew:\n    uri: file:somewhere\n"
    # a document that ends with a comment block keeps it at the end, with the new section set
    # apart by the empty lines that led the block
    assert extend("a:\n    x: 1\n\n\n# end of file\n") == (
        "a:\n    x: 1\n\n\nnew:\n    uri: file:somewhere\n\n\n# end of file\n"
    )
    # a setting added to an existing section is not a new section, so nothing is set apart
    doc = pyre.config.newYamlEditor(text="a:\n    x: 1\n\nb:\n    y: 2\n")
    doc.set("b", "z", value=3)
    assert doc.render() == "a:\n    x: 1\n\nb:\n    y: 2\n    z: 3\n"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
