#! /usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A known keyword whose value cannot be converted lands in the extras as text, with a warning,
    rather than aborting the read
    """
    # access the package
    import pyre
    import journal

    # for a header in memory
    import io

    # the warning is expected; quiet it
    journal.warning("pyre.envi.header").active = False

    # a header with a bad line count and a bad wavelength list
    text = "\n".join(
        [
            "ENVI",
            "samples = 10",
            "lines = many",
            "wavelength = {0.4, blue, 0.6}",
            "",
        ]
    )
    # parse it
    hdr = pyre.envi.reader().parse(stream=io.StringIO(text), uri="memory")

    # the good field made it
    assert hdr.samples == 10
    # the bad ones did not
    assert hdr.lines is None
    assert hdr.wavelength is None
    # and their text is in the bag, a bare value as a string and a braced one as a list
    assert hdr.extras == {"lines": "many", "wavelength": ["0.4", "blue", "0.6"]}

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
