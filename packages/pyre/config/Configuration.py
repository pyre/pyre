# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Configuration:
    """
    A temporary holding place for configuration events

    The various codecs build and populate instances of this class as part of the ingestion of
    configuration sources. They provide a temporary holding place to store the harvested events
    until the entire source is processed without errors. This way, the configuation retrieved
    from the source will be known to be at least syntactically correct without the risk of
    polluting the global framework configuration data structures with partial input from
    invalid sources.
    """


    # public data
    events = None


    # interface
    def newAssignment(self, key, value, locator):
        """
        Create a new assignment event and add it to the queue
        """
        self.events.append(self.Assignment(key=key, value=value, locator=locator))
        return


    def newSource(self, source, locator):
        """
        Create a new instruction to process a configuration source and add it to the queue
        """
        self.events.append(self.Source(source=source, locator=locator))


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.events = []
        return


    # types
    class Event:
        """The base class for all configuration events"""

        # public data
        locator = None

        # meta methods
        def __init__(self, locator, **kwds):
            super().__init__(**kwds)
            self.locator = locator
            return

    class Assignment(Event):
        """A request to bind a {key} to a {value}"""

        # public data
        key = None
        value = None

        # interface
        def identify(self, inspector, **kwds):
            """Ask {inspector} to process an {Assignment}"""
            return inspector.bind(key=self.key, value=self.value, locator=self.locator, **kwds)

        # meta methods
        def __init__(self, key, value, **kwds):
            super().__init__(**kwds)
            self.key = key
            self.value = value
            return

        def __str__(self):
            return "{{{0}: {1} <- {2}}}".format(self.locator, ".".join(self.key), self.value)

    class Source(Event):
        """A request to load configuration settings from a named source"""

        # public data
        source = None

        # interface
        def identify(self, inspector, **kwds):
            """Ask {inspector} to process a {Source} event"""
            return inspector.load(source=self.source, locator=self.locator, **kwds)

        # meta methods
        def __init__(self, source, **kwds):
            super().__init__(**kwds)
            self.source = source
            return

        def __str__(self):
            return "{{{0.locator}: loading {0.source}}".format(self)

# end of file 
