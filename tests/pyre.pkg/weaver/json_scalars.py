#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the JSON renderer leaves the values JSON holds as they are
"""


def test() -> None:
    """
    Render nothing, truth values, numbers and text
    """
    # support
    import pyre

    # make a renderer
    renderer = pyre.weaver.json()
    # the schemata
    schemata = pyre.schemata

    # each schema and its value
    cases = [
        (schemata.bool(), False),
        (schemata.int(), 7),
        (schemata.float(), 2.5),
        (schemata.str(), "x{y}"),
        (schemata.int(), None),
    ]
    # go through them
    for schema, value in cases:
        # each value
        rendered = renderer.render(schema=schema, value=value)
        # is left as it is
        assert rendered is value or rendered == value, (schema.typename, rendered)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
