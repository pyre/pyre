#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the JSON renderer turns arrays into nested lists, with their numbers intact
"""


def test() -> None:
    """
    Render a flat array, a nested one, and an empty one
    """
    # support
    import pyre

    # make a renderer
    renderer = pyre.weaver.json()
    # and an array of floats
    schema = pyre.schemata.array()

    # a flat array
    assert renderer.render(schema=schema, value=(1.0, 2.0)) == [1.0, 2.0]
    # a nested one
    nested = renderer.render(schema=schema, value=((1.0, 2.0), (3.0, 4.0)))
    # keeps its levels
    assert nested == [[1.0, 2.0], [3.0, 4.0]], nested
    # and an empty one is an empty list
    assert renderer.render(schema=schema, value=()) == []

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
