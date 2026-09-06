#! /usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Parse, render, and use the georeferencing record
    """
    # access the package
    import pyre

    # a geographic record
    text = "Geographic Lat/Lon, 1, 1, -180, 90, 0.5, 0.25, WGS-84, units=Degrees"
    # parse
    info = pyre.envi.mapInfo.parse(text=text)
    # check the fixed items
    assert info.projection == "Geographic Lat/Lon"
    assert info.pixel == (1.0, 1.0)
    assert info.coordinates == (-180.0, 90.0)
    assert info.size == (0.5, 0.25)
    # and the projection dependent ones
    assert info.extras == ["WGS-84", "units=Degrees"]
    assert info.settings() == {"units": "Degrees"}
    # the reference pixel maps to the origin of the image
    assert info.toPixel(x=-180.0, y=90.0) == (0.0, 0.0)
    # a point one pixel to the east and two to the south
    assert info.toPixel(x=-179.5, y=89.5) == (2.0, 1.0)
    # and back
    assert info.toMap(line=2.0, sample=1.0) == (-179.5, 89.5)
    # rendering reproduces the text
    assert info.render() == text
    assert str(info) == text

    # a UTM record, with a zone and hemisphere
    text = "UTM, 1.5, 1.5, 500000, 4000000, 30, 30, 11, North, WGS-84, units=Meters"
    # parse
    info = pyre.envi.mapInfo.parse(text=text)
    # the reference pixel is the center of the first pixel
    assert info.pixel == (1.5, 1.5)
    assert info.extras == ["11", "North", "WGS-84", "units=Meters"]
    # and rendering reproduces the text
    assert info.render() == text

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
