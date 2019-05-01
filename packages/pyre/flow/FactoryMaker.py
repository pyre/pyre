# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# framework
import pyre
# my superclass
from .FlowMaster import FlowMaster
# the product protocol
from .Specification import Specification


# declaration
class FactoryMaker(FlowMaster):
    """
    The meta-class of flow nodes
    """


    # methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build a new factory record
        """
        # augment the attributes
        attributes["pyre_inputs"] = ()
        attributes["pyre_outputs"] = ()
        # chain up to build the record
        factory = super().__new__(cls, name, bases, attributes, **kwds)
        # and pass it on
        return factory


    def __init__(self, name, bases, attributes, **kwds):
        """
        Initialize a new factory record
        """
        # chain up
        super().__init__(name, bases, attributes, **kwds)
        # if this is an internal record
        if self.pyre_internal:
            # all done
            return

        # make piles for inputs and outputs
        inputs = []
        outputs = []
        # go through my facilities, looking for products
        for trait in self.pyre_facilities():
            # if this is a product
            if issubclass(trait.protocol, Specification):
                # and it's an input
                if trait.input:
                    # add it to the pile of inputs
                    inputs.append(trait)
                # if it's an output
                if trait.output:
                    # add it to the pile of outputs
                    outputs.append(trait)
        # attach them
        self.pyre_inputs = tuple(inputs)
        self.pyre_outputs = tuple(outputs)

        # all done
        return


# end of file
