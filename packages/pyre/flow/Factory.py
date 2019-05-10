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
        # get my inventory
        inventory = self.pyre_inventory
        # get my inputs
        inputs = (inventory[trait].value for trait in self.pyre_inputs)
        # bind me to them
        self.pyre_bindInputs(*inputs)
        # get my outputs
        outputs = (inventory[trait].value for trait in self.pyre_outputs)
        # bind me to them
        self.pyre_bindOutputs(*outputs)
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


    def pyre_bindInputs(self, *inputs):
        """
        Bind me to the sequence of products in {inputs}
        """
        # get my status monitor
        monitor = self.pyre_status
        # go through each of my inputs
        for product in inputs:
            # tell the product i'm interested in its state
            product.pyre_addInputBinding(factory=self)
            # and notify my monitor
            monitor.addInputBinding(factory=self, product=product)
        # all done
        return self


    def pyre_unbindInputs(self, *inputs):
        """
        Unbind me to the sequence of products in {inputs}
        """
        # get my status monitor
        monitor = self.pyre_status
        # go through each of my inputs
        for product in inputs:
            # tell the product i'm interested in its state
            product.pyre_removeInputBinding(factory=self)
            # and notify my monitor
            monitor.removeInputBinding(factory=self, product=product)
        # all done
        return self


    def pyre_bindOutputs(self, *outputs):
        """
        Bind me to the sequence of products in {outputs}
        """
        # get my status monitor
        monitor = self.pyre_status
        # go through the products
        for product in outputs:
            # tell the product i'm its factory
            product.pyre_addOutputBinding(factory=self)
            # and notify my monitor
            monitor.addOutputBinding(factory=self, product=product)
        # all done
        return self


    def pyre_unbindOutputs(self, *outputs):
        """
        Unbind me to the sequence of products in {outputs}
        """
        # get my status monitor
        monitor = self.pyre_status
        # go through the products
        for product in outputs:
            # tell the product i'm not its factory any more
            product.pyre_removeOutputBinding(factory=self)
            # and notify my monitor
            monitor.removeOutputBinding(factory=self, product=product)
        # all done
        return self


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
            # if {old} is non-trivial
            if old is not None:
                # remove from my input pile
                self.pyre_unbindInputs(old)
            # if {new} is non-trivial
            if new is not None:
                # add it to my pile of inputs
                self.pyre_bindInputs(new)

        # if {trait} is an output
        if trait.output:
            # if {old} is non-trivial
            if old is not None:
                # ask it to forget me
                self.pyre_unbindOutputs(old)
            # if {new} is non-trivial
            if new is not None:
                # tell it i'm one of its factories
                self.pyre_bindOutputs(new)
        # chain up
        return super().pyre_traitModified(trait=trait, new=new, old=old)


    # debugging support
    def pyre_dump(self, channel, indent=''):
        """
        Put some useful info about me in {channel}
        """
        # sign on
        channel.line(f"{indent}{self}")

        # my inputs
        channel.line(f"{indent*2}inputs:")
        for product in self.pyre_inputs:
            channel.line(f"{indent*3}{product}")

        # my outputs
        channel.line(f"{indent*2}outputs:")
        for product in self.pyre_outputs:
            channel.line(f"{indent*3}{product}")

        # my status monitor
        channel.line(f"{indent*2}status: {self.pyre_status}")
        channel.line(f"{indent*3}observers:")
        for observer in self.pyre_status.observers:
            channel.line(f"{indent*4}{observer}")

        # all done
        return self


# end of file
