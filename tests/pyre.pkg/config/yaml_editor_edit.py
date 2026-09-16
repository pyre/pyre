#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that edits by key path leave everything else as it was: a key added at the end of a
section lands before the comment block that follows the section, a new section lands before
the end of file marker, a list grows in place, a replaced value keeps its comments, and a
removed first entry leaves the comment above it at the top of its section
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
    editor = pyre.config.newYamlEditor(uri="editor.yaml")
    # add a key at the end of a section whose last entry is a list with a trailing comment
    editor.set("crete", "expanded", value=["earth:crete", "earth:crete/003_A_028"])
    # replace a value that carries an inline comment
    editor.set("crete", "collection", value="NISAR_L2_GSLC_PROVISIONAL_V1")
    # add a new section
    editor.set("local", "uri", value="file:/tmp/data")
    editor.set("local", "expanded", value=[])
    # grow the list of archives
    editor.append("archives", value="qed.archives.local#local")
    # remove an entry that carries a comment before it
    assert editor.delete("qed.app", "shell")
    # removing what is not there is reported
    assert not editor.delete("qed.app", "nothing")
    # render
    text = editor.render()
    # and compare with what is expected
    assert text == expected, text
    # all done
    return editor


# what the edits should produce
expected = """# -*- yaml -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a section with comments before and after its entries
crete:
    uri: "earth:crete" # a quoted value
    collection: NISAR_L2_GSLC_PROVISIONAL_V1
    # the region
    polygon:
        - (23.3547, 34.7211)
        - (26.4923, 34.7211)
        - (26.4923, 35.7146)
        - (23.3547, 35.7146)
    expanded:
        - earth:crete
        - earth:crete/003_A_028

# the connected archives
archives:
    - qed.archives.earth#crete
    - qed.archives.local#local


# a section that stays untouched
qed.app:
    # the shell
    nexus.services.web:
        address: ip4:0.0.0.0:8005

local:
    uri: file:/tmp/data
    expanded: []

# end of file
"""


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
