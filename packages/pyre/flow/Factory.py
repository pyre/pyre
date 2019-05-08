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
    def pyre_make(self, product, context=None):
        """
        Construct my products
        """
        # put a plan together
        stale = tuple(self.pyre_plan(context=context))
        # go through the stale products
        for product in stale:
            # force them to get remade
            product.pyre_make()
        # if any of my inputs were stale
        if stale:
            # invoke me
            self.pyre_run(requestor=product, stale=stale)
        # all done
        return self


    @pyre.export
    def pyre_plan(self, context=None):
        """
        Describe what needs to get done to make my products
        """
        # grab my inventory
        inventory = self.pyre_inventory
        # go through my inputs
        for trait in self.pyre_inputs:
            # get the product
            product = inventory[trait].value
            # if it's stale
            if product.pyre_stale:
                # it needs to be remade
                yield product
        # all done
        return


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # introduce my inputs to my monitor
        self.pyre_bindInputs()
        # introduce my monitor to my outputs
        self.pyre_bindOutputs()
        # all done
        return


    # flow hooks
    def pyre_newStatus(self, **kwds):
        """
        Build a handler for my status changes
        """
        # grab the factory
        from .FactoryStatus import FactoryStatus
        # make one and return it
        return FactoryStatus(**kwds)


    def pyre_run(self, requestor, stale, **kwds):
        """
        Invoke me and remake my products
        """
        # nothing to do
        return self


    # framework hooks
    def pyre_traitModified(self, trait, new, old):
        """
        Hook invoked when a trait changes value
        """
        # get my status monitor
        status = self.pyre_status
        # if {trait} is an input
        if trait.input:
            # ask my status monitor to replace the {old} input with a {new} one
            status.replaceInput(new=new, old=old)
        # if {trait} is an output
        if trait.output:
            # ask my status monitor to replace the {old} output with a {new} one
            status.replaceOutput(new=new, old=old)
        # chain up
        return super().pyre_traitModified(trait=trait, new=new, old=old)


    # implementation details
    def pyre_monitors(self, pile):
        """
        Yield the sequence of monitors of traits in {pile}
        """
        # get my inventory
        inventory = self.pyre_inventory
        # go through my inputs
        for trait in pile:
            # look up the associated slot
            slot = inventory[trait]
            # get the product
            product = slot.value
            # and return its status monitor
            yield product.pyre_status

        # all done
        return


    def pyre_bindInputs(self):
        """
        Bind me to the current value of my outputs
        """
        # delegate to my status monitor
        return self.pyre_status.bindInputs(factory=self)


    def pyre_bindOutputs(self):
        """
        Bind me to the current value of my outputs
        """
        # grab my inventory
        inventory = self.pyre_inventory
        # go through my inputs
        for trait in self.pyre_outputs:
            # get the associated product
            product = inventory[trait].value
            # register me as a factory
            product.pyre_registerFactory(factory=self)
        # all done
        return



# end of file
