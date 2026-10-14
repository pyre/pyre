#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that containers render: a list puts its items on lines of their own, a list nested in a
list fits on the line of its item, and a mapping fits on one line, with its values
"""


def test() -> None:
    """
    Render a list, a list of lists, and a mapping
    """
    # support
    import pyre.schemata

    # a renderer that records what it is asked to write
    class Renderer:
        """
        A stand-in for the renderers of the weaver
        """

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

    # make a renderer
    renderer = Renderer()

    # a list of strings
    strings = pyre.schemata.list(schema=pyre.schemata.str())
    # named the way a trait would be
    strings.name = "strings"
    # puts its name on a line, and each of its items on a line of its own
    assert list(strings.render(renderer=renderer, value=["a", "b"])) == ["strings = ", "a,", "b,"]

    # a list of lists of strings
    nested = pyre.schemata.list(schema=pyre.schemata.list(schema=pyre.schemata.str()))
    # named the way a trait would be
    nested.name = "nested"
    # renders each inner list on the line of its item
    assert len(list(nested.render(renderer=renderer, value=[["a", "b"]]))) == 2

    # a mapping of strings
    mapping = pyre.schemata.mapping(schema=pyre.schemata.str())
    # named the way a trait would be
    mapping.name = "selection"
    # fits on one line, in its text form
    assert list(mapping.render(renderer=renderer, value={"band": "L", "frequency": "A"})) == [
        "selection = band:L, frequency:A"
    ]

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
