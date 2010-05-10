# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Event import Event


class Assignment(Event):
    """
    A request to bind a {key} to a {value}
    """


    # public data
    key = None
    value = None
    locator = None


    # interface
    def identify(self, inspector, **kwds):
        """
        Ask {inspector} to process this event
        """
        return inspector.bind(key=self.key, value=self.value, locator=self.locator, **kwds)


    # meta methods
    def __init__(self, key, value, locator, **kwds):
        super().__init__(**kwds)
        self.key = key
        self.value = value
        self.locator = locator
        return


    def __str__(self):
        return "{{{0}: {1} <- {2}}}".format(self.locator, ".".join(self.key), self.value)


# end of file 
