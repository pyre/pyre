# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# support
import pyre
# protocols
from .Producer import Producer
from .Specification import Specification


# class declaration
class Workflow(pyre.application, family='pyre.applications.workflow'):
    """
    A simple application class for managing workflows
    """


    # user configurable state
    factories = pyre.properties.set(schema=Producer())
    factories.doc = "the set of flow factories"

    products = pyre.properties.set(schema=Specification())
    products.doc = "the set of flow products"


    # debugging support
    def pyre_dump(self):
        """
        Display my factories and products
        """
        # make a channel
        channel = self.info
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
