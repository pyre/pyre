#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the block that trails a document, e.g. its closing comment, stays at the end however
the sections that are added before it end: a section whose last entry is an empty collection
holds the block while the collection waits for an entry, and the section that follows takes it
from there, so nothing is ever placed after the closing comment
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None

    # a document with one section and a closing comment
    text = "\n".join(["# -*- pyre -*-", "", "a:", "    x: 1", "", "", "# end of file", ""])

    # add sections one entry at a time, the first ending in a scalar, the way a writer that
    # knows nothing about the layout of the file would
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("b", "y", value=2)
    doc.set("c", "z", value=3)
    # the closing comment is still the last line
    reference = doc.render()
    assert reference.splitlines()[-1] == "# end of file"

    # the same sections, with the first ending in an empty mapping
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("b", "y", value=2)
    doc.set("b", "s", value={})
    doc.set("c", "z", value=3)
    lines = doc.render().splitlines()
    # the closing comment is the last line
    assert lines[-1] == "# end of file"
    # and the sections are set apart just like the ones that end in a scalar
    at = lines.index("    s: {}")
    assert lines[at + 1 : at + 4] == ["", "", "c:"]

    # the same sections, with the first ending in an empty list
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("b", "y", value=2)
    doc.set("b", "p", value=[])
    doc.set("c", "z", value=3)
    lines = doc.render().splitlines()
    # the closing comment is the last line
    assert lines[-1] == "# end of file"
    # and the sections are set apart just like the ones that end in a scalar
    at = lines.index("    p: []")
    assert lines[at + 1 : at + 4] == ["", "", "c:"]

    # a chain of sections that each end in an empty collection
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("b", "s", value={})
    doc.set("c", "p", value=[])
    doc.set("d", "z", value=3)
    rendered = doc.render()
    lines = rendered.splitlines()
    # keeps the closing comment last
    assert lines[-1] == "# end of file"
    # with the sections in the order they were added
    assert [line for line in lines if line.endswith(":")] == ["a:", "b:", "c:", "d:"]
    # and reads back into a document that renders the same
    assert pyre.config.newYamlEditor(text=rendered).render() == rendered

    # all done
    return doc


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
