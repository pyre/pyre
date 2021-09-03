# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset


# class declaration
class Unrecognizable(Asset,
                     family="merlin.projects.foreign.unrecognizable",
                     implements=merlin.protocols.foreign):
    """
    Encapsulation of an auxiliary file
    """


# end of file
