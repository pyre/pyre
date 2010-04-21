# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Event import Event


class ConfigurationSource(Event):
    """
    A request to load settings from some source
    """


    # public data
    source = None
    locator = None


    # interface
    def identify(self, inspector, **kwds):
        """
        Ask {inspector} to process this event
        """
        return inspector.load(source=self.source, locator=self.locator, **kwds)


    # meta methods
    def __init__(self, source, locator, **kwds):
        super().__init__(**kwds)
        self.source = source
        self.locator = locator
        return


    def __str__(self):
        return "{{{0.locator}: loading {0.source}}".format(self)


# end of file 
