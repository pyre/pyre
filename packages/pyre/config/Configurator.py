# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections


class Configurator(object):
    """
    """


    # public data
    events = ()


    # interface
    def createAssignment(self, key, value, locator):
        """
        Create an event that corresponds to an assignment of {value} to {key}, and insert it
        into the event queue
        """
        from .Assignment import Assignment
        assignment = Assignment(key=key, value=value, locator=locator)
        self.events.append(assignment)
        return assignment


    def populate(self, calculator):
        """
        Convert assignment events into bound variables
        """
        # loop over the binding and create the associated variable assignments
        while self.events:
            event = self.events.popleft()
            calculator.bind(name=event.key, value=event.value, locator=event.locator)
        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # variable assignment storage: an unbounded, double-ended queue
        self.events = collections.deque()

        return


# end of file 
