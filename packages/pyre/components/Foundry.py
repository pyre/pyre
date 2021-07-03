# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import collections
# framework
import pyre


# mark a callable as a factory of components
class Foundry(pyre.patterns.decorator):
    """
    A decorator for callables that return component classes
    """


    # public data
    pyre_tip = '' # a short description of what this component does
    pyre_implements = None # the protocols implemented by this component


    # meta-methods
    def __init__(self, factory, implements=None, tip='', **kwds):
        # chain up
        super().__init__(factory=factory, **kwds)
        # save the tip
        self.pyre_tip = tip
        # and the sequence of implemented protocols
        self.pyre_implements = self.sequify(implements)
        # all done
        return


    def __call__(self, *args, **kwds):
        # invoke the factory to get the component class
        component = super().__call__(*args, **kwds)
        # decorate it with my tip
        component.pyre_tip = self.pyre_tip
        # and return it
        return component


    # implementation details
    @classmethod
    def sequify(self, items):
        """
        Normalize {items} into a tuple
        """
        # take care of {None} and anything false or empty
        if not items: return ()
        # if {items} is any iterable
        if isinstance(items, collections.abc.Iterable):
            # turn it into a tuple
            return tuple(items)
        # otherwise, place the lone item into a tuple
        return (items,)


# end of file
