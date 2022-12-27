#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def generate():
    """
    Generate the color table
    """
    # open the rgb file
    rgb = open("rgb.txt")
    # go through the contents
    for line in rgb:
        # pull the information
        r,g,b, name = line.strip().split(None, 3)
        # build the statement
        yield f"    \"{name}\": CSI.csi24(red={r}, green={g}, blue={b}),"
    # all done
    return


def preamble():
    """
    The opening lines of the file
    """
    return (
        """# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# get the control sequence generator
from .CSI import CSI


# the table of color names to ANSI control sequences
table = {
    # the reset sequence
    "normal": CSI.reset(),

    # the X11 named colors""")


def postamble():
    """
    Return the trailing lines
    """
    return """    }

# end of file"""


# bootstrap
if __name__ == "__main__":
    # open the output file
    x11 = open("ANSI_x11.py", "w")

    # place the preamble
    print(preamble(), file=x11)
    print("\n".join(generate()), file=x11)
    print(postamble(), file=x11)


# end of file
