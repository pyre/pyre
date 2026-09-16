#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A walk through the round trip editor of yaml documents

The editor reads a configuration file, lets you inspect and change it by key path, and writes
it back with everything you did not touch exactly as it was: comments, blank lines, quoting,
and the order of entries all survive. Run this script from this directory; it reads
{app.yaml}, shows what each operation changes, and writes the result to {app-edited.yaml},
leaving the original alone
"""

# externals
import difflib

# support
import pyre.config


def show(step, before, after):
    """
    Print what {step} changed, as a diff of the rendered document
    """
    # the banner
    print(f"\n== {step}")
    # the diff, without the file headers
    lines = list(difflib.unified_diff(before.splitlines(), after.splitlines(), lineterm="", n=1))
    # if nothing changed
    if not lines:
        # say so
        print("   (no change)")
        # all done
        return
    # otherwise, print the hunks
    for line in lines[2:]:
        # indented
        print(f"   {line}")
    # all done
    return


def main():
    """
    The walkthrough
    """
    # the editor lives in the yaml package of {pyre.config}; the backend is {ruamel.yaml}, and
    # the editor knows whether it is available
    from pyre.config.yaml import editor

    # if it is not
    if not editor.available():
        # there is nothing to show
        print("the editor needs 'ruamel.yaml', which is not importable in this environment")
        # all done
        return 1

    # open the document; the factory takes a {uri}, or {text} to work on a string
    doc = pyre.config.newYamlEditor(uri="app.yaml")
    # keep the original rendering for the diffs below
    original = doc.render()
    # a document that goes through the editor untouched comes out byte for byte the same
    assert original == open("app.yaml", encoding="utf-8").read()

    # reading: {get} takes a key path, the literal keys of the document, and a default
    print("== reading")
    print(f"   crete/uri: {doc.get('crete', 'uri')!r}")
    print(f"   crete/polygon: {list(doc.get('crete', 'polygon'))}")
    print(f"   archives: {list(doc.get('archives'))}")
    # keys with dots in them are single keys, as they are in the file
    print(f"   qed.app/shell: {doc.get('qed.app', 'shell')!r}")
    print(
        f"   qed.app/nexus.services.web/address: {doc.get('qed.app', 'nexus.services.web', 'address')!r}"
    )
    # a path that leads nowhere yields the default
    print(f"   crete/missing: {doc.get('crete', 'missing', default='<unset>')!r}")

    # replacing a value: the entry stays where it is, and its inline comment survives
    before = doc.render()
    doc.set("crete", "collection", value="NISAR_L2_GSLC_PROVISIONAL_V1")
    show("replace a value", before, doc.render())

    # adding a key to a section: it goes at the end of the section, and the comment block
    # that followed the section stays after it
    before = doc.render()
    doc.set("crete", "expanded", value=["earth:crete", "earth:crete/003_A_028"])
    show("add a key at the end of a section", before, doc.render())

    # growing a list
    before = doc.render()
    doc.append("archives", value="qed.archives.local#scratch")
    show("append to a list", before, doc.render())

    # a new section: the mappings along the path are made as needed, and a new top level
    # section lands before the end of file marker, set apart by a blank line
    before = doc.render()
    doc.set("scratch", "uri", value="file:/tmp/scratch")
    doc.set("scratch", "expanded", value=[])
    show("add a new section", before, doc.render())

    # removing entries: {delete} takes a key path and reports whether the entry was there;
    # {remove} takes a list item by value
    before = doc.render()
    assert doc.delete("qed.app", "shell")
    assert not doc.delete("qed.app", "shell")
    assert doc.remove("archives", value="qed.archives.earth#crete")
    show("delete a key and remove a list item", before, doc.render())

    # removing a whole section
    before = doc.render()
    assert doc.delete("crete")
    show("delete a section", before, doc.render())

    # mistakes are reported: an empty path names nothing, and a key cannot go under a scalar
    for step, path in (
        ("empty path", ()),
        ("key under a scalar", ("qed.app", "nexus.services.web", "address", "deeper")),
    ):
        try:
            doc.set(*path, value=1)
        except doc.EditingError as error:
            print(f"\n== {step}: refused: {error}")

    # saving: the document is written all at once, to the location it was read from unless
    # another is given; here the original is left alone
    doc.save(uri="app-edited.yaml")
    print("\n== saved to app-edited.yaml")
    # and the whole trip
    show("everything, from the original", original, doc.render())
    # all done
    return 0


# main
if __name__ == "__main__":
    # run
    raise SystemExit(main())


# end of file
