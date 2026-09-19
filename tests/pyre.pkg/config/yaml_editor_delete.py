#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check where the comments of a removed entry go: the block that trailed a removed section
stays where it was, whether the section was first or in the middle; a comment on the line of
a removed entry goes with it; a mapping emptied by a removal becomes a bare key that carries
the block and takes new keys later; and a list emptied by a removal keeps its brackets while
the block moves above it
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None
    # the fixture header, common to every outcome
    header = open("editor.yaml", encoding="utf-8").read().split("# a section with comments")[0]
    # go through the scenarios
    for label, edits, tail in scenarios:
        # open the fixture
        doc = pyre.config.newYamlEditor(uri="editor.yaml")
        # apply the edits
        for operation, path, value in edits:
            # each in its own way
            if operation == "delete":
                assert doc.delete(*path), label
            elif operation == "remove":
                assert doc.remove(*path, value=value), label
            else:
                doc.set(*path, value=value)
        # render
        text = doc.render()
        # and compare
        assert text == header + tail, f"{label}:\n{text}"
    # all done
    return


# the scenarios: a label, the edits, and the expected text after the fixture header
scenarios = [
    (
        "the first section",
        [("delete", ("crete",), None)],
        """# a section with comments before and after its entries

# the connected archives
archives:
    - qed.archives.earth#crete


# a section that stays untouched
qed.app:
    # the shell
    shell: web
    nexus.services.web:
        address: ip4:0.0.0.0:8005

# end of file
""",
    ),
    (
        "a section in the middle",
        [("delete", ("archives",), None)],
        """# a section with comments before and after its entries
crete:
    uri: "earth:crete" # a quoted value
    collection: NISAR_L2_GCOV_PROVISIONAL_V1
    # the region
    polygon:
        - (23.3547, 34.7211)
        - (26.4923, 34.7211)
        - (26.4923, 35.7146)
        - (23.3547, 35.7146)

# the connected archives


# a section that stays untouched
qed.app:
    # the shell
    shell: web
    nexus.services.web:
        address: ip4:0.0.0.0:8005

# end of file
""",
    ),
    (
        "an entry with an inline comment",
        [("delete", ("crete", "uri"), None)],
        """# a section with comments before and after its entries
crete:
    collection: NISAR_L2_GCOV_PROVISIONAL_V1
    # the region
    polygon:
        - (23.3547, 34.7211)
        - (26.4923, 34.7211)
        - (26.4923, 35.7146)
        - (23.3547, 35.7146)

# the connected archives
archives:
    - qed.archives.earth#crete


# a section that stays untouched
qed.app:
    # the shell
    shell: web
    nexus.services.web:
        address: ip4:0.0.0.0:8005

# end of file
""",
    ),
    (
        "the last leaf of a nested mapping, then a new key under the bare key",
        [
            ("delete", ("qed.app", "nexus.services.web", "address"), None),
            ("set", ("qed.app", "nexus.services.web", "port"), 8080),
        ],
        """# a section with comments before and after its entries
crete:
    uri: "earth:crete" # a quoted value
    collection: NISAR_L2_GCOV_PROVISIONAL_V1
    # the region
    polygon:
        - (23.3547, 34.7211)
        - (26.4923, 34.7211)
        - (26.4923, 35.7146)
        - (23.3547, 35.7146)

# the connected archives
archives:
    - qed.archives.earth#crete


# a section that stays untouched
qed.app:
    # the shell
    shell: web
    nexus.services.web:
        port: 8080

# end of file
""",
    ),
    (
        "the only item of a list",
        [("remove", ("archives",), "qed.archives.earth#crete")],
        """# a section with comments before and after its entries
crete:
    uri: "earth:crete" # a quoted value
    collection: NISAR_L2_GCOV_PROVISIONAL_V1
    # the region
    polygon:
        - (23.3547, 34.7211)
        - (26.4923, 34.7211)
        - (26.4923, 35.7146)
        - (23.3547, 35.7146)

# the connected archives
archives: []


# a section that stays untouched
qed.app:
    # the shell
    shell: web
    nexus.services.web:
        address: ip4:0.0.0.0:8005

# end of file
""",
    ),
]


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
