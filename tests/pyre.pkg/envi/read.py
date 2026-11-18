#!/usr/bin/env python3
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

    # the layout: samples
    assert hdr.samples == 43200
    # lines
    assert hdr.lines == 21600
    # bands
    assert hdr.bands == 3
    # the offset to the data
    assert hdr.headerOffset == 128
    # which the header also reports as its offset
    assert hdr.offset == 128
    # the kind of file
    assert hdr.fileType == "ENVI Standard"
    # the data type code
    assert hdr.dataType == 12
    # and the cell it names
    assert hdr.datatype == "uint16"
    # the interleave, folded to lower case
    assert hdr.interleave == "bil"
    # and puts the bands in the middle
    assert hdr.shape == (21600, 3, 43200)
    # the byte order
    assert hdr.byteOrder == 0

    # the braced text keeps its punctuation, including the sign the parser splits on
    assert hdr.description == "sample ENVI header; with a comma, and an = sign"
    # the georeferencing, as it is spelled in the file
    assert hdr.mapInfo.startswith("Arbitrary, 1, 1, -180.00138889")
    # parsed
    info = hdr.map()
    # names its projection
    assert info.projection == "Arbitrary"
    # the reference pixel
    assert info.pixel == (1.0, 1.0)
    # its map coordinates
    assert info.coordinates == (-180.00138889, 90.00138889)
    # the size of a pixel
    assert info.size == (0.00833333, 0.00833333)
    # and the rest of the record
    assert info.extras == ["0", "North"]
    # and renders back to the text in the file
    assert info.render() == hdr.mapInfo

    # a braced list that spans lines
    assert hdr.bandNames == ["Band 1", "Band 2", "Band 3"]
    # per-band values: the wavelengths
    assert hdr.wavelength == [0.45, 0.55, 0.65]
    # and their widths
    assert hdr.fwhm == [0.01, 0.02, 0.03]
    # scalars: the coordinates of the first pixel
    assert hdr.xStart == 12.5
    # in both directions
    assert hdr.yStart == 7.0
    # and the value that marks missing data
    assert hdr.dataIgnore == -9999.0
    # text: the time of the acquisition
    assert hdr.acquisitionTime == "2011-09-18T16:32:57Z"
    # and the sensor
    assert hdr.sensorType == "Unknown"

    # keywords the standard does not define land in the bag: bare values as strings, braced
    # ones as lists of strings
    assert hdr.extras == {"custom scalar": "42", "custom list": ["a", "b", "c"]}

    # fields the sample never mentions are unset: the classes
    assert hdr.classes is None
    # the elevation model
    assert hdr.dem is None
    # and the bad band list
    assert hdr.bbl is None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
