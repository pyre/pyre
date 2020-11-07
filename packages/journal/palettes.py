# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved


# get the ANSI color spaces
from .ANSI import ANSI


# the null palette provides no decoration
null = {
    "reset": "",
    "debug": "",
    "firewall": "",
    "info": "",
    "warning": "",
    "error": "",
    "body": "",
    }


# the light palette looks reasonable against a light background
light = {
    # set the colors
    "reset": ANSI.x11(name="normal"),
    "debug": ANSI.x11(name="blue"),
    "firewall": ANSI.x11(name="fuchsia"),
    "info": ANSI.x11(name="forest green"),
    "warning": ANSI.x11(name="orange"),
    "error": ANSI.x11(name="red"),
    "body": ANSI.x11(name="normal"),
    }


# the dark palette looks reasonable against a dark background
dark = {
    # set the colors
    "reset": ANSI.x11(name="normal"),
    "debug": ANSI.x11(name="cornflower blue"),
    "firewall": ANSI.x11(name="fuchsia"),
    "info": ANSI.x11(name="forest green"),
    "warning": ANSI.x11(name="orange"),
    "error": ANSI.x11(name="red"),
    "body": ANSI.x11(name="normal"),
}


# end of file
