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


    def __init__(self, **kwds):
        super().__init__(**kwds)
        # event storage: an unbounded, double-ended queue
        self.events = collections.deque()

        return


# end of file 
