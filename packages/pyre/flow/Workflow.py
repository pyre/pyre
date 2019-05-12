# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# support
import pyre
# protocols
from .Flow import Flow
from .Producer import Producer
from .Specification import Specification
# my superclass
from .Factory import Factory


# class declaration
class Workflow(Factory, family='pyre.flow.workflow', implements=Flow):
    """
    A container of flow products and factories
    """


    # user configurable state
    factories = pyre.properties.set(schema=Producer())
    factories.doc = "the set of my factories"

    products = pyre.properties.set(schema=Specification())
    products.doc = "the set of my products"


    # debugging support
    def pyre_dump(self, channel=None):
        """
        Display my factories and products
        """
        # make a channel
        channel = self.info if channel is None else channel
        # sign on
        channel.line("flo:")
        # first, the products
        channel.line("  products:")
        for product in self.products:
            channel.line(f"    {product}")
        # and the factories
        channel.line("  factories:")
        for factory in self.factories:
            channel.line(f"    {factory}")
        # flush
        channel.log()

        # all done
        return


# end of file
