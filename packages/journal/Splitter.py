# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Device import Device


# forward messages to a collection of device
class Splitter(Device):
    """
    Journal device that manages and feeds a collection of devices
    """


# end of file
