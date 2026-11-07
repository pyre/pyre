#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the bound timeline keeps its epoch, makes instants from their seconds past it, and
measures the time between them
"""


def test():
    """
    Make a timeline and a few instants on it
    """
    # access the geometry bindings
    from pyre.extensions.pyre import geometry

    # a timeline on the unix epoch
    unix = geometry.Timeline()
    # has its epoch at zero
    assert unix.epoch == 0
    # and one whose epoch is a day later
    later = geometry.Timeline(epoch=86400)
    # remembers it
    assert later.epoch == 86400

    # an instant an hour past the epoch
    hour = unix.point(coordinate=3600)
    # knows its coordinate
    assert hour.coordinate == 3600
    # and equals another made the same way
    assert hour == unix.point(coordinate=3600)
    # but not one made elsewhere
    assert hour != unix.point(coordinate=7200)
    # the two are an hour apart
    assert unix.distance(p=hour, q=unix.point(coordinate=7200)) == 3600

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
