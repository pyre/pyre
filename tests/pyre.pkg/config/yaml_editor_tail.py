#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an empty list at the end of a section stays inside the section: the empty lines and
the comments that set the section apart from the next one belong after the list, not between
the list and the rest of the section, where they would leave the list running into whatever
follows

An empty list cannot carry the block that follows it, and as the last entry of its section it
has no sibling to hand the block to; the block goes to the entry that follows the section
"""


def test():
    # support
    import pyre.config
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None

    # a document with sections that end in a list, in a scalar, and in a section of their own,
    # set apart by empty lines, and in one case by a comment as well
    text = "\n".join(
        [
            "# the first archive",
            "crete:",
            "    uri: earth:crete",
            "    polygon:",
            "        - (23.3547, 34.7211)",
            "        - (26.4923, 34.7211)",
            "",
            "# the second archive",
            "rolling:",
            "    uri: s3://bucket/products",
            "    region: us-west-2",
            "",
            "app:",
            "    shell: web",
            "    services:",
            "        web:",
            "            address: ip4:0.0.0.0:8005",
            "",
            "",
            "archives:",
            "    - qed.archives.s3#rolling",
            "",
        ]
    )

    # a new empty list at the end of a section that ends in a list
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("crete", "expanded", value=[])
    lines = doc.render().splitlines()
    # it sits right under the last entry of its section
    assert lines.index("    expanded: []") == lines.index("        - (26.4923, 34.7211)") + 1
    # followed by the empty line, and then the comment and the key of the next section
    at = lines.index("    expanded: []")
    assert lines[at + 1 : at + 4] == ["", "# the second archive", "rolling:"]

    # a new empty list at the end of a section that ends in a scalar
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("rolling", "expanded", value=[])
    lines = doc.render().splitlines()
    at = lines.index("    expanded: []")
    assert lines[at - 1] == "    region: us-west-2"
    assert lines[at + 1 : at + 3] == ["", "app:"]

    # a new empty list at the end of a section that is itself the end of a section: the entry
    # that follows is two levels up, past both
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("app", "services", "web", "aliases", value=[])
    lines = doc.render().splitlines()
    at = lines.index("            aliases: []")
    assert lines[at - 1] == "            address: ip4:0.0.0.0:8005"
    assert lines[at + 1 : at + 4] == ["", "", "archives:"]

    # a list at the end of a section that goes from populated to empty and back
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("rolling", "expanded", value=["s3://bucket/products"])
    populated = doc.render()
    lines = populated.splitlines()
    at = lines.index("        - s3://bucket/products")
    assert lines[at - 1] == "    expanded:"
    assert lines[at + 1 : at + 3] == ["", "app:"]
    # empty it, the way the next edit of the file would
    doc = pyre.config.newYamlEditor(text=populated)
    doc.set("rolling", "expanded", value=[])
    emptied = doc.render()
    lines = emptied.splitlines()
    at = lines.index("    expanded: []")
    assert lines[at - 1] == "    region: us-west-2"
    assert lines[at + 1 : at + 3] == ["", "app:"]
    # empty it by removing its only item instead, which takes another path through the editor
    doc = pyre.config.newYamlEditor(text=populated)
    assert doc.remove("rolling", "expanded", value="s3://bucket/products") is True
    assert doc.render() == emptied
    # populate it again, and it is back where it was
    doc = pyre.config.newYamlEditor(text=emptied)
    doc.set("rolling", "expanded", value=["s3://bucket/products"])
    assert doc.render() == populated

    # removing the entries restores the document to the character, however they got there
    doc = pyre.config.newYamlEditor(text=text)
    doc.set("crete", "expanded", value=[])
    doc.set("rolling", "expanded", value=[])
    doc.set("app", "services", "web", "aliases", value=[])
    doc = pyre.config.newYamlEditor(text=doc.render())
    doc.delete("crete", "expanded")
    doc.delete("rolling", "expanded")
    doc.delete("app", "services", "web", "aliases")
    assert doc.render() == text

    # the empty lines that follow a section survive the removal of its last entry, whatever
    # kind of entry that is; they set the next section apart, and that does not change
    doc = pyre.config.newYamlEditor(text=text)
    doc.delete("rolling", "region")
    lines = doc.render().splitlines()
    at = lines.index("    uri: s3://bucket/products")
    assert lines[at + 1 : at + 3] == ["", "app:"]
    # while removing an entry from the middle of a section leaves no hole behind
    doc = pyre.config.newYamlEditor(text=text)
    doc.delete("rolling", "uri")
    lines = doc.render().splitlines()
    at = lines.index("rolling:")
    assert lines[at + 1 : at + 4] == ["    region: us-west-2", "", "app:"]

    # an empty list at the very end of the document has nothing after it to hand its block to,
    # and keeps whatever trails the document after its brackets
    doc = pyre.config.newYamlEditor(text="a:\n    x: 1\n\n\n# end of file\n")
    doc.set("a", "items", value=[])
    assert doc.render() == "a:\n    x: 1\n    items: []\n\n\n# end of file\n"

    # all done
    return doc


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
