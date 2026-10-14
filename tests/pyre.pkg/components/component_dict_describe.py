#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a component describes its dict traits: as json, as a configuration summary, and as
rendered configuration, keeping secret tables out of all of them
"""


def test() -> None:
    """
    Describe a component with dict traits
    """
    # support
    import json
    import pyre

    # a component with a table and a secret table
    class Reader(pyre.component, family="pyre.tests.dict.describe.reader"):
        """
        A component with dict traits
        """

        # a table of strings
        selection = pyre.properties.kv()
        # and a secret one
        credentials = pyre.properties.kv()
        credentials.secret = True

    # make a reader
    reader = Reader(name="reader")
    # with tables
    reader.selection = {"band": "L", "frequency": "A"}
    reader.credentials = {"token": "hunter2"}

    # its description
    doc = reader.pyre_renderConfiguration()
    # can be written as json
    text = json.dumps(doc)
    # and holds the table
    assert doc["properties"]["selection"]["value"] == {"band": "L", "frequency": "A"}
    # but not the secret one
    assert doc["properties"]["credentials"]["value"] is None
    assert "hunter2" not in text

    # its configuration summary
    summary = "\n".join(reader.pyre_showConfiguration())
    # shows the table
    assert "band" in summary
    # but not the secret one
    assert "hunter2" not in summary

    # a renderer that writes traits as assignments
    class Renderer:
        """
        A stand-in for the renderers of the weaver
        """

        # the start of a component
        def componentStart(self, component):
            """
            Render the name of {component}
            """
            # as a section
            yield f"{component.pyre_name}:"

        # the end of a component
        def componentEnd(self, component):
            """
            Close the section of {component}
            """
            # with a blank line
            yield ""

        # a trait and its value
        def trait(self, name: str, value) -> str:
            """
            Render the {name} of a trait and its {value}
            """
            # as an assignment
            return f"{name} = {value}"

        # a value on a line of its own
        def value(self, value) -> str:
            """
            Render a {value}
            """
            # as it is
            return f"{value}"

    # its rendered configuration
    rendered = list(reader.pyre_renderTraitValues(renderer=Renderer()))
    # holds the table, in its text form
    assert "selection = band:L, frequency:A" in rendered, rendered
    # and leaves the secret one out
    assert not any("credentials" in line or "hunter2" in line for line in rendered), rendered

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
