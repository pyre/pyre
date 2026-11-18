#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Build headers directly and check what they derive from their fields
    """
    # access the package
    import pyre

    # a bare header
    hdr = pyre.envi.header()
    # knows nothing: no shape
    assert hdr.shape is None
    # no data type
    assert hdr.datatype is None
    # no offset
    assert hdr.offset == 0
    # no georeferencing
    assert hdr.map() is None
    # and no extras
    assert hdr.extras == {}

    # a single band product is a plane, whatever the interleave says
    hdr = pyre.envi.header(lines=4, samples=5, bands=1, interleave="bip")
    # so its shape has two axes
    assert hdr.shape == (4, 5)
    # and so is one that never mentions bands
    hdr = pyre.envi.header(lines=4, samples=5)
    # so its shape has two axes too
    assert hdr.shape == (4, 5)

    # a multi-band product puts the band axis where the interleave says: a band sequential one
    hdr = pyre.envi.header(lines=4, samples=5, bands=3, interleave="bsq")
    # puts it first
    assert hdr.shape == (3, 4, 5)
    # a band interleaved by line one
    hdr = pyre.envi.header(lines=4, samples=5, bands=3, interleave="bil")
    # puts it in the middle
    assert hdr.shape == (4, 3, 5)
    # and a band interleaved by pixel one
    hdr = pyre.envi.header(lines=4, samples=5, bands=3, interleave="bip")
    # puts it last
    assert hdr.shape == (4, 5, 3)
    # and defaults to band sequential
    hdr = pyre.envi.header(lines=4, samples=5, bands=3)
    # so the bands come first
    assert hdr.shape == (3, 4, 5)
    # the interleave
    hdr = pyre.envi.header(interleave="BSQ")
    # is folded to lower case on the way in
    assert hdr.interleave == "bsq"

    # every ENVI data type code names a pyre cell
    codes = {
        1: "uint8",
        2: "int16",
        3: "int32",
        4: "float32",
        5: "float64",
        6: "complex64",
        9: "complex128",
        12: "uint16",
        13: "uint32",
        14: "int64",
        15: "uint64",
    }
    # check them all
    for code, name in codes.items():
        # through the header
        assert pyre.envi.header(dataType=code).datatype == name

    # the cell name carries the byte order marker the header calls for: big endian
    assert pyre.envi.header(dataType=12, byteOrder=1).cell == "uint16be"
    # little endian
    assert pyre.envi.header(dataType=12, byteOrder=0).cell == "uint16le"
    # and for complex cells too
    assert pyre.envi.header(dataType=6, byteOrder=1).cell == "complex64be"
    # without a byte order it is the native cell
    assert pyre.envi.header(dataType=12).cell == "uint16"
    # a single byte scalar has no order
    assert pyre.envi.header(dataType=1, byteOrder=1).cell == "uint8"
    # and without a data type there is no cell
    assert pyre.envi.header(byteOrder=1).cell is None

    # the header offset
    hdr = pyre.envi.header(headerOffset=128)
    # becomes the offset to the data
    assert hdr.offset == 128
    # the ENVI spellings work as keywords too, since the framework matches by alias: set
    # each one
    hdr = pyre.envi.header(**{"header offset": 256, "data type": 4, "byte order": 1})
    # and check that they landed: the offset
    assert hdr.offset == 256
    # the data type
    assert hdr.datatype == "float32"
    # and the byte order
    assert hdr.byteOrder == 1

    # extras
    hdr = pyre.envi.header(extras={"custom": "value"})
    # ride along intact
    assert hdr.extras == {"custom": "value"}

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
