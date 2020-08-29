# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved


# superclass
from .Splitter import Splitter


# write messages to the console and a set of other devices
class Tee(Splitter):
    """
    Journal device that writes messages to the console as well as to a set of other devices
    """


# end of file
