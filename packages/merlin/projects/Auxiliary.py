# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset


# class declaration
class Auxiliary(Asset,
                family="merlin.projects.auxiliaries.auxiliary",
                implements=merlin.protocols.auxiliary):
    """
    Encapsulation of an auxiliary file
    """


# end of file
