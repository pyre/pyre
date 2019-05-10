# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import weakref
# support
import pyre
# my protocol
from .Specification import Specification
# my superclass
from .Node import Node


# class declaration
class Product(Node, implements=Specification, internal=True):
    """
    The base class for data products
    """


    # public data
    @property
    def pyre_stale(self):
        """
        Retrieve my status
        """
        # delegate to my status manager
        return self.pyre_status.stale

    @pyre_stale.setter
    def pyre_stale(self, value):
        """
        Set my status
        """
        # delegate to my status manager
        self.pyre_status.stale = value
        # all done
        return


    # protocol obligations
    @pyre.export
    def pyre_make(self):
        """
        Invoke my factories to update me
        """
        # if i am not stale
        if not self.pyre_stale:
            # nothing to do
            return self
        # otherwise, go through my factories
        for factory in self.pyre_factories:
            # and ask each one to update me
            factory.pyre_make(product=self)
        # if all went well, update my status
        self.pyre_stale = False
        # all done
        return self


    def sync(self):
        """
        Examine my state
        """


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the list of my factories
        self.pyre_factories = weakref.WeakSet()
        # all done
        return


    # flow hooks
    def pyre_newStatus(self, **kwds):
        """
        Build a handler for my status changes
        """
        # grab the factory
        from .ProductStatus import ProductStatus
        # make one and return it
        return ProductStatus(**kwds)


    def pyre_addInputBinding(self, factory):
        """
        Bind me as an input to the given {factory}
        """
        # let my monitor know there is a new client {factory}
        self.pyre_status.addInputBinding(factory=factory, product=self)
        # all done
        return


    def pyre_removeInputBinding(self, factory):
        """
        Unbind me as an input to the given {factory}
        """
        # let my monitor know there is a new client {factory}
        self.pyre_status.removeInputBinding(factory=factory, product=self)
        # all done
        return


    def pyre_addOutputBinding(self, factory):
        """
        Bind me as an output to the given {factory}
        """
        # add {factory} to my pile
        self.pyre_factories.add(factory)
        # let my monitor know there is a new client {factory}
        self.pyre_status.addOutputBinding(factory=factory, product=self)
        # all done
        return


    def pyre_removeOutputBinding(self, factory):
        """
        Unbind me as an output to the given {factory}
        """
        # remove {factory} from my pile
        self.pyre_factories.remove(factory)
        # let my monitor know there is a new client {factory}
        self.pyre_status.removeOutputBinding(factory=factory, product=self)
        # all done
        return


    # debugging support
    def pyre_dump(self, channel, indent=''):
        """
        Put some useful info about me in {channel}
        """
        # sign on
        channel.line(f"{indent}{self}")

        # my factories
        channel.line(f"{indent*2}factories:")
        for factory in self.pyre_factories:
            channel.line(f"{indent*3}{factory}")

        # my state
        channel.line(f"{indent*2}stale: {self.pyre_stale}")

        # my status monitor
        channel.line(f"{indent*2}status: {self.pyre_status}")
        channel.line(f"{indent*3}observers:")
        for observer in self.pyre_status.observers:
            channel.line(f"{indent*4}{observer}")

        # all done
        return self


# end of file
