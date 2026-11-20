#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the JSON renderer turns mappings into tables, with each value rendered the way the
schema of the entries says
"""


def test() -> None:
    """
    Render a mapping of integers and one of dates
    """
    # support
    import datetime
    import pyre

    # make a renderer
    renderer = pyre.weaver.json()
    # the schemata
    schemata = pyre.schemata

    # a mapping of integers keeps its numbers
    integers = renderer.render(schema=schemata.mapping(schema=schemata.int()), value={"one": 1})
    # entry by entry
    assert integers == {"one": 1}, integers
    # and the values of a mapping of dates
    days = renderer.render(
        schema=schemata.mapping(schema=schemata.date()),
        value={"launch": datetime.date(2025, 7, 30)},
    )
    # are rendered as dates
    assert days == {"launch": "2025-07-30"}, days

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
