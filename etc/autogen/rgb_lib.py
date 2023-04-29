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
        yield f"    table[\"{name}\"] = csi_t::csi24({r}, {g}, {b});"
    # all done
    return


def preamble():
    """
    The opening lines of the file
    """
    return (
        """// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the forward declarations
#include "forward.h"
// external support
#include "externals.h"
// get the support we need
#include "ASCII.h"
#include "CSI.h"
#include "ANSI.h"


// the color table factory
auto
pyre::journal::ANSI::
make_x11() -> table_type
{
    // make a table
    table_type table;

    // the reset sequence
    table["normal"] = csi_t::reset();

    // the X11 named colors""")


def postamble():
    """
    Return the trailing lines
    """
    return """
    // all done
    return table;
}


// end of file"""


# bootstrap
if __name__ == "__main__":
    # open the output file
    x11 = open("ANSI_x11.cc", "w")

    # place the preamble
    print(preamble(), file=x11)
    print("\n".join(generate()), file=x11)
    print(postamble(), file=x11)


# end of file
