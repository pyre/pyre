# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre

# access the requirements
from .Device import Device
# and their defaults
from .Console import Console


# declaration
class Journal(pyre.component, family="journal"):
    """
    Place holder for the configurable bits of the journal package
    """


    # class public data
    device = pyre.properties.facility(interface=Device, default=Console)
    device.doc = "the component responsible for handling journal entries"


# end of file 
