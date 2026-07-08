#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that components can be instantiated
"""


def test():
    import pyre

    # declare
    class component(pyre.component):
        """a trivial component"""

        p = pyre.property()

    # attempt to instantiate
    c = component(name="c")
    # verify that the extent is recorded properly
    assert set(c.pyre_getExtent()) == {c}

    return c


# main
if __name__ == "__main__":
    test()


# end of file
