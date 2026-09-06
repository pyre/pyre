#! /usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Read a sample header and check that every field landed where it should, converted to its
    type
    """
    # access the package
    import pyre

    # read the sample
    hdr = pyre.envi.reader().read(uri="sample.hdr")

    # the layout
    assert hdr.samples == 43200
    assert hdr.lines == 21600
    assert hdr.bands == 3
    assert hdr.headerOffset == 128
    assert hdr.offset == 128
    assert hdr.fileType == "ENVI Standard"
    assert hdr.dataType == 12
    assert hdr.datatype == "uint16"
    # the interleave is folded to lower case
    assert hdr.interleave == "bil"
    assert hdr.shape == (21600, 3, 43200)
    assert hdr.byteOrder == 0

    # the braced text keeps its punctuation, including the sign the parser splits on
    assert hdr.description == "sample ENVI header; with a comma, and an = sign"
    # the georeferencing
    assert hdr.mapInfo.startswith("Arbitrary, 1, 1, -180.00138889")
    info = hdr.map()
    assert info.projection == "Arbitrary"
    assert info.pixel == (1.0, 1.0)
    assert info.coordinates == (-180.00138889, 90.00138889)
    assert info.size == (0.00833333, 0.00833333)
    assert info.extras == ["0", "North"]
    # and renders back to the text in the file
    assert info.render() == hdr.mapInfo

    # a braced list that spans lines
    assert hdr.bandNames == ["Band 1", "Band 2", "Band 3"]
    # per-band values
    assert hdr.wavelength == [0.45, 0.55, 0.65]
    assert hdr.fwhm == [0.01, 0.02, 0.03]
    # scalars
    assert hdr.xStart == 12.5
    assert hdr.yStart == 7.0
    assert hdr.dataIgnore == -9999.0
    # text
    assert hdr.acquisitionTime == "2011-09-18T16:32:57Z"
    assert hdr.sensorType == "Unknown"

    # keywords the standard does not define land in the bag: bare values as strings, braced
    # ones as lists of strings
    assert hdr.extras == {"custom scalar": "42", "custom list": ["a", "b", "c"]}

    # fields the sample never mentions are unset
    assert hdr.classes is None
    assert hdr.dem is None
    assert hdr.bbl is None

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
