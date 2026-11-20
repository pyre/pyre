#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the YAML renderer turns containers into lists and tables, with each entry rendered
the way the schema of the entries says
"""


def test() -> None:
    """
    Render a set, an array and a mapping
    """
    # support
    import pyre

    # make a renderer
    renderer = pyre.weaver.yaml()
    # the schemata
    schemata = pyre.schemata

    # a set of strings
    words = renderer.render(schema=schemata.set(schema=schemata.str()), value={"{a}"})
    # becomes a list of escaped text
    assert words == ["{{a}}"], words
    # an array
    matrix = renderer.render(schema=schemata.array(), value=((1.0, 0.0), (0.0, 1.0)))
    # becomes nested lists of numbers
    assert matrix == [[1.0, 0.0], [0.0, 1.0]], matrix
    # and a mapping of integers
    counts = renderer.render(schema=schemata.mapping(schema=schemata.int()), value={"one": 1})
    # becomes a table of numbers
    assert counts == {"one": 1}, counts

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
