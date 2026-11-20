#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the JSON renderer turns every sequence into a list, with each entry rendered the way
the schema of the entries says
"""


def test() -> None:
    """
    Render lists, tuples and sets
    """
    # support
    import datetime
    import pyre

    # make a renderer
    renderer = pyre.weaver.json()
    # the schemata
    schemata = pyre.schemata

    # a list of integers keeps its numbers
    assert renderer.render(schema=schemata.list(schema=schemata.int()), value=[1, 2]) == [1, 2]
    # a tuple of floats becomes a list
    floats = renderer.render(schema=schemata.tuple(schema=schemata.float()), value=(1.0, 2.5))
    # with its numbers intact
    assert floats == [1.0, 2.5], floats
    # a set becomes a list too
    words = renderer.render(schema=schemata.set(schema=schemata.str()), value={"a", "b"})
    # of the same entries
    assert sorted(words) == ["a", "b"], words
    # and the entries of a list of dates
    days = renderer.render(
        schema=schemata.list(schema=schemata.date()), value=[datetime.date(2026, 11, 20)]
    )
    # are rendered as dates
    assert days == ["2026-11-20"], days

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
