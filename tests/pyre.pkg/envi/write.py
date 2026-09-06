#! /usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def render():
    """
    Render a header and read it back; every field must survive the round trip
    """
    # access the package
    import pyre

    # for headers in memory
    import io

    # build a header with a bit of everything
    hdr = pyre.envi.header(
        description="a product; with punctuation, and an = sign",
        samples=5,
        lines=4,
        bands=3,
        headerOffset=0,
        fileType="ENVI Standard",
        dataType=4,
        interleave="bsq",
        byteOrder=1,
        mapInfo="UTM, 1, 1, 500000, 4000000, 30, 30, 11, North, WGS-84, units=Meters",
        bandNames=["red", "green", "blue"],
        wavelength=[0.65, 0.55, 0.45],
        fwhm=[0.01, 0.01, 0.01],
        xStart=1.5,
        yStart=2.0,
        dataIgnore=-9999.0,
        defaultBands=[1, 2, 3],
        extras={"custom scalar": "42", "custom list": ["a", "b"]},
    )
    # render it
    text = pyre.envi.writer().render(header=hdr)
    # the text opens with the marker
    assert text.startswith("ENVI\n")
    # spells keywords the ENVI way
    assert "\nheader offset = 0\n" in text
    assert "\ndata ignore value = -9999.0\n" in text
    # braces text fields and sequences, and leaves scalars bare
    assert "\ndescription = {a product; with punctuation, and an = sign}\n" in text
    assert "\nband names = {red, green, blue}\n" in text
    assert "\nfile type = ENVI Standard\n" in text
    assert "\ninterleave = bsq\n" in text
    # and carries the extras
    assert "\ncustom scalar = 42\n" in text
    assert "\ncustom list = {a, b}\n" in text

    # read it back
    copy = pyre.envi.reader().parse(stream=io.StringIO(text), uri="memory")
    # every trait must match
    for trait in pyre.envi.header.pyre_traits():
        # compare
        assert getattr(copy, trait.name) == getattr(hdr, trait.name), trait.name
    # and so must the extras
    assert copy.extras == hdr.extras
    # the georeferencing round trips too
    assert copy.map().settings() == {"units": "Meters"}

    # all done
    return


def write():
    """
    Write a header to a file and read it back
    """
    # access the package
    import pyre

    # the scratch product
    uri = "envi_write_test.hdr"
    # a header
    hdr = pyre.envi.header(samples=5, lines=4, dataType=12, interleave="bip")
    # write it
    pyre.envi.writer().write(header=hdr, uri=uri)
    # read it back
    copy = pyre.envi.reader().read(uri=uri)
    # check
    assert copy.shape == (4, 5)
    assert copy.datatype == "uint16"
    assert copy.interleave == "bip"

    # all done
    return


# main
if __name__ == "__main__":
    # run the tests
    render()
    write()


# end of file
