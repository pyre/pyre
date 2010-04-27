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
    def configure(self, executive, override=True):
        """
        Iterate through the event queue and carry out the 0
        """
        # access the calculator
        calculator = executive.calculator
        # loop over the binding and create the associated variable assignments
        while self.events:
            event = self.events.popleft()
            event.identify(inspector=self, executive=executive, override=override)
        # all done
        return

 
    # event processing
    def bind(self, executive, key, value, locator, override, **kwds):
        """
        Record a new variable binding with the {executive}
        """
        return executive.calculator.bind(name=key, value=value, locator=locator, override=override)


    def load(self, executive, source, locator, **kwds):
        """
        Ask the {executive} to load the configuration settings in {source}
        """
        return executive.loadConfiguration(uri=source, locator=locator)


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

        return


# end of file 
