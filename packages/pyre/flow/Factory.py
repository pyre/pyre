# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# support
import pyre
# my protocol
from .Producer import Producer
# my superclass
from .Node import Node
# my meta-class
from .FactoryMaker import FactoryMaker


# class declaration
class Factory(Node, metaclass=FactoryMaker, implements=Producer, internal=True):
    """
    The base class for creators of data products
    """

    # public data
    pyre_inputs = ()
    pyre_outputs = ()


    # interface obligations
    @pyre.export
    def make(self, context=None):
        """
        Construct my products
        """
        # don't know much
        return self


    @pyre.export
    def plan(self, context=None):
        """
        Describe what needs to get to done to make my products
        """
        # don't know how to do that
        return


# end of file
