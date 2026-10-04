#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the block that trails a document is split by level when an entry is added: the
backend files every comment after the last entry of the document with the deepest entry, so the
block mixes lines that belong to the levels of the tree, e.g. an entry that was commented out of
a list, with lines that belong to the document, e.g. its closing comment. A new entry goes after
the lines of its own level and the levels below it, and ahead of the lines of the levels above
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None

    # a list with an item that was commented out, followed by the closing comment of the document
    text = "\n".join(
        [
            "workspace:",
            "    expanded:",
            "        - file:/data",
            "",
            "archives:",
            "    - local#workspace",
            "    # - s3#rolling",
            "",
            "",
            "# end of file",
            "",
        ]
    )
    # connect an archive the way the server does: register it, then configure it
    doc = pyre.config.newYamlEditor(text=text)
    doc.append("archives", value="s3#s3:rolling")
    doc.set("s3:rolling", value={"uri": "s3://bucket/products"})
    rendered = doc.render()
    # the item that was commented out stays in the list, ahead of the new item; the new
    # section follows the list, and the closing comment stays last
    assert rendered == "\n".join(
        [
            "workspace:",
            "    expanded:",
            "        - file:/data",
            "",
            "archives:",
            "    - local#workspace",
            "    # - s3#rolling",
            "    - s3#s3:rolling",
            "",
            "",
            "s3:rolling:",
            "    uri: s3://bucket/products",
            "",
            "",
            "# end of file",
            "",
        ]
    )
    # and the document reads back into one that renders the same
    assert pyre.config.newYamlEditor(text=rendered).render() == rendered

    # a block with lines at every level of a nested section
    text = "\n".join(
        [
            "a:",
            "    b:",
            "        x: 1",
            "        # y: 2",
            "    # c: 3",
            "# d: 4",
            "",
            "",
            "# end of file",
            "",
        ]
    )
    # an entry at the deepest level
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("a", "b", "z", value=5)
    # goes after the line of its level, and ahead of the lines of the levels above
    assert doc.render().splitlines()[:6] == [
        "a:",
        "    b:",
        "        x: 1",
        "        # y: 2",
        "        z: 5",
        "    # c: 3",
    ]
    # an entry at the middle level
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("a", "e", value=6)
    # goes after the lines of its level and the level below it
    assert doc.render().splitlines()[:7] == [
        "a:",
        "    b:",
        "        x: 1",
        "        # y: 2",
        "    # c: 3",
        "    e: 6",
        "# d: 4",
    ]
    # a new section
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("f", value=7)
    rendered = doc.render()
    # goes after the section that was commented out right below the last one, set apart from
    # it the way the document sets its sections apart, and ahead of the closing comment
    assert rendered == "\n".join(
        [
            "a:",
            "    b:",
            "        x: 1",
            "        # y: 2",
            "    # c: 3",
            "# d: 4",
            "",
            "",
            "f: 7",
            "",
            "",
            "# end of file",
            "",
        ]
    )
    # and the document reads back into one that renders the same
    assert pyre.config.newYamlEditor(text=rendered).render() == rendered

    # all done
    return doc


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
