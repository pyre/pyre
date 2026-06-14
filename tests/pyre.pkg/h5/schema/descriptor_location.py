#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the {location} class keyword declares the absolute mount point of a root
group, that subclasses inherit it, and that ordinary groups default to {None}
"""


# the driver
def test():
    # support
    import pyre

    # a root group that declares its absolute mount point
    class LSAR(pyre.h5.schema.group, location="/science/LSAR"):
        """
        An L-band product root
        """

    # a product that subclasses it without redeclaring the mount
    class RSLC(LSAR):
        """
        A product derived from the band base
        """

    # an ordinary group declares no mount
    class Plain(pyre.h5.schema.group):
        """
        A group with no mount
        """

    # the root records its mount
    assert LSAR._pyre_location == "/science/LSAR"
    # subclasses inherit it
    assert RSLC._pyre_location == "/science/LSAR"
    # ordinary groups default to {None}
    assert Plain._pyre_location is None

    # instances see the mount through their class
    assert LSAR(name="root")._pyre_location == "/science/LSAR"
    assert RSLC(name="root")._pyre_location == "/science/LSAR"
    assert Plain(name="root")._pyre_location is None

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
