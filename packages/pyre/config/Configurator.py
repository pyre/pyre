# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections
from ..patterns.Named import Named


class Configurator(Named):
    """
    """


    # public data
    sources = ()
    bindings = ()


    # interface
    def createAssignment(self, key, value, locator):
        """
        Create an event that corresponds to an assignment of {value} to {key}, and insert it
        into the event queue
        """
        from .Assignment import Assignment
        assignment = Assignment(key=key, value=value, locator=locator)
        self.bindings.append(assignment)
        return assignment


    def populate(self, calculator):
        """
        Convert assignment events into bound variables
        """
        # loop over the binding and create the associated variable assignments
        for event in self.bindings:
            calculator.bind(name=event.key, value=event.value, locator=event.locator)
        # all done
        return


    def __init__(self, name=None, **kwds):
        name = name if name is not None else "pyre.configurator"
        super().__init__(name=name, **kwds)
        # variable assignment storage: an unbounded, double-ended queue
        self.bindings = collections.deque()
        # configuration sources
        self.sources = collections.deque(
            ["pml://pyre/system/pyre.pml", "pml://pyre/user/pyre.pml"]
            )

        return


# end of file 
