#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the chroma bindings: converters, serializers, and the palette
    """
    # get the framework
    import pyre

    # there is nothing to check if the bindings were not built into this configuration
    if pyre.libpyre is None:
        # so quietly succeed
        return

    # reach the chroma bindings
    chroma = pyre.libpyre.chroma

    # {hsl} at hue zero, full saturation, mid luminosity is pure red
    red = chroma.rgb.hsl(0, 1, 0.5)
    # and its channels come through as named attributes
    assert (red.red, red.green, red.blue) == (1.0, 0.0, 0.0)

    # the same color built directly compares equal
    assert chroma.Color(1, 0, 0) == red

    # {ansi} renders it as a 24-bit truecolor escape
    assert chroma.ansi.rgb(red) == "\x1b[38;2;255;0;0m"
    # and the reset sequence is the canonical one
    assert chroma.ansi.reset() == "\x1b[0m"

    # the palette resolves a canonical name to that same color
    assert chroma.rgb.palette.find("red") == red
    # and reports a miss as {None}
    assert chroma.rgb.palette.find("not-a-color") is None

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
