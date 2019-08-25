# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import itertools
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


    # persistence
    def save(self):
        """
        Save my entire graph
        """
        # make a weaver
        weaver = pyre.weaver.weaver()
        # set the encoding
        weaver.language = self.encoding
        # open a file
        with open(f"{self.pyre_name}.{self.encoding}", mode='w') as stream:
            # assemble the document
            document = self.pyre_renderTraitValues(renderer=weaver.language)
            # get the weaver to do its things
            for line in weaver.weave(document=document):
                # place each line in the file
                print(line, file=stream)
        # all done
        return


    # debugging support
    def pyre_dump(self, channel=None, indent=' '*2, level=0):
        """
        Display my factories and products
        """
        # make a channel, if necessary
        channel = self.info if channel is None else channel
        # sign on
        super().pyre_dump(channel=channel, indent=indent, level=level)

        # compute the margin
        margin = indent * (level+1)

        # display the products
        channel.line(f"{margin}products:")
        for product in self.products:
            channel.line(f"{margin}{indent}{product}")

        # and the factories
        channel.line(f"{margin}factories:")
        for factory in self.factories:
            channel.line(f"{margin}{indent}{factory}")

        # flush
        channel.log()
        # all done
        return self


    # constants
    encoding = 'pfg'


# end of file
