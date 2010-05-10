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
    counter = None


    # interface
    def configure(self, executive, priority):
        """
        Iterate through the event queue and carry out the associated actions
        """
        # access the calculator
        calculator = executive.calculator
        # loop over the binding and create the associated variable assignments
        while self.events:
            # get the event
            event = self.events.popleft()
            # get its sequence number
            seq = (priority, self.counter[priority])
            # update the counter
            self.counter[priority] += 1
            # and process the event
            event.identify(inspector=self, executive=executive, priority=seq)
        # all done
        return

 
    # event processing
    def bind(self, executive, key, value, locator, priority, **kwds):
        """
        Record a new variable binding with the {executive}
        """
        return executive.calculator.bind(key=key, value=value, locator=locator, priority=priority)


    def load(self, executive, source, locator, **kwds):
        """
        Ask the {executive} to load the configuration settings in {source}
        """
        return executive.loadConfiguration(
            uri=source, priority=executive.USER_CONFIGURATION, locator=locator)


    # interface for harvesting events from configuration files
    def recordAssignment(self, key, value, locator):
        """
        Create an event that corresponds to an assignment of {value} to {key}, and insert it
        into the event queue
        """
        from .Assignment import Assignment
        assignment = Assignment(key=key, value=value, locator=locator)
        self.events.append(assignment)
        return assignment


    def recordConfigurationSource(self, source, locator):
        """
        Create an event that corresponds to a request to load a configuration file
        """
        from .ConfigurationSource import ConfigurationSource
        event = ConfigurationSource(source, locator)
        self.events.append(event)
        return event


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # variable assignment storage: an unbounded, double-ended queue
        self.events = collections.deque()
        # and the event priority counter
        self.counter = collections.Counter()

        return


# end of file 
