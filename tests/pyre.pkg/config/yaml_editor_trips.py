#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a section that comes and goes leaves the document as it found it: the empty lines
that set sections apart must not pile up with every trip, and a separation that was made for a
section must not outlive it

When a section is added at the end of a document, the empty lines ahead of whatever trails the
document stay behind, to set the new section apart. When the section is removed, the block that
trailed it comes back with empty lines of its own. These are one separation, not two
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None

    # add a section at the end of a document, and remove it in a later session
    def trip(text):
        # load the document
        doc = pyre.config.newYamlEditor(text=text)
        # add a section
        doc.set("visitor", "uri", value="file:somewhere")
        # read the result back, the way the next edit of the file would
        doc = pyre.config.newYamlEditor(text=doc.render())
        # remove the section
        assert doc.delete("visitor") is True
        # and hand off the text
        return doc.render()

    # the documents: closing comments behind one and two empty lines, nothing at all after
    # the last section, with one section and with two, and sections that are set apart
    # differently from the closing comment
    documents = [
        "a:\n    x: 1\n\n\n# end of file\n",
        "a:\n    x: 1\n\n# end of file\n",
        "a:\n    x: 1\n",
        "a:\n    x: 1\n\nc:\n    z: 3\n",
        "a:\n    x: 1\n\nc:\n    z: 3\n\n\n# end of file\n",
    ]
    # go through them
    for text in documents:
        # the trip leaves each one as it was
        assert trip(text) == text, repr(trip(text))

    # and keeps doing so, however many times it is made
    text = documents[0]
    current = text
    for _ in range(10):
        current = trip(current)
    assert current == text

    # the empty lines at the end of a document are its author's, and they survive the removal
    # of the last section; the wider of the two separations involved stands
    doc = pyre.config.newYamlEditor(text="a:\n    x: 1\n\nb:\n    y: 2\n\n\n")
    doc.delete("b")
    assert doc.render() == "a:\n    x: 1\n\n\n"

    # a block that has something to say is not a separation, and what follows is added to it
    doc = pyre.config.newYamlEditor(text="a:\n    x: 1\n# about a\n\nb:\n    y: 2\n\n# end\n")
    doc.delete("b")
    assert doc.render() == "a:\n    x: 1\n# about a\n\n\n# end\n"

    # all done
    return doc


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
