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
        Describe what needs to get done to make my products
        """
        # don't know how to do that
        return


    # framework hooks
    def pyre_traitModified(self, trait, new, old):
        """
        Hook invoked when a trait changes value
        """
        print(trait)
        # chain up
        return super().pyre_traitModified(trait=trait, new=new, old=old)


# end of file
