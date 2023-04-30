# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# framework
import merlin


# base class for merlin factories
class Factory(merlin.flow.factory, implements=merlin.protocols.producer, internal=True):
    """
    The base class for {merlin} factories
    """


# end of file
