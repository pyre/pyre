#! /usr/bin/env python3
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

    # for unique instance names
    import itertools

    # keyword construction needs a named instance, and each name is one instance
    counter = itertools.count()
    # so build every header under a fresh name
    make = lambda **kwds: pyre.envi.header(name=f"header-{next(counter)}", **kwds)

    # a bare header knows nothing
    hdr = pyre.envi.header()
    assert hdr.shape is None
    assert hdr.datatype is None
    assert hdr.offset == 0
    assert hdr.map() is None
    assert hdr.extras == {}

    # a single band product is a plane, whatever the interleave says
    hdr = make(lines=4, samples=5, bands=1, interleave="bip")
    assert hdr.shape == (4, 5)
    # and so is one that never mentions bands
    hdr = make(lines=4, samples=5)
    assert hdr.shape == (4, 5)

    # a multi-band product puts the band axis where the interleave says
    hdr = make(lines=4, samples=5, bands=3, interleave="bsq")
    assert hdr.shape == (3, 4, 5)
    hdr = make(lines=4, samples=5, bands=3, interleave="bil")
    assert hdr.shape == (4, 3, 5)
    hdr = make(lines=4, samples=5, bands=3, interleave="bip")
    assert hdr.shape == (4, 5, 3)
    # and defaults to band sequential
    hdr = make(lines=4, samples=5, bands=3)
    assert hdr.shape == (3, 4, 5)
    # the interleave is folded to lower case on the way in
    hdr = make(interleave="BSQ")
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
        assert make(dataType=code).datatype == name

    # the header offset survives
    hdr = make(headerOffset=128)
    assert hdr.offset == 128
    # and the ENVI spellings work as keywords too, since the framework matches by alias
    hdr = make(**{"header offset": 256, "data type": 4, "byte order": 1})
    assert hdr.offset == 256
    assert hdr.datatype == "float32"
    assert hdr.byteOrder == 1

    # extras ride along
    hdr = make(extras={"custom": "value"})
    assert hdr.extras == {"custom": "value"}

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
