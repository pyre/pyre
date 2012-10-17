# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class PyreError(Exception):
    """
    Base class for all pyre related errors
    """

    def __init__(self, description, locator=None, **kwds):
        super().__init__(**kwds)
        self.description = description
        self.locator = locator
        return

    def __str__(self):
        # if we have a locator
        if self.locator:
            # give it a chance to pinpoint the error
            return "{}: {}".format(self.locator, self.description)
        # otherwise
        return self.description


class FrameworkError(PyreError):
    """
    Base class for all framework exceptions

    Useful when you are trying to catch any and all pyre framework errors
    """


class BadResourceLocatorError(FrameworkError):
    """
    Exception raised when a URI is not formed properly
    """

    def __init__(self, uri, reason, **kwds):
        self.uri = uri
        self.reason = reason
        super().__init__(description="{!r}: {}".format(str(self.uri), self.reason), **kwds)
        return


class ComponentNotFoundError(FrameworkError):

    def __init__(self, uri, **kwds):
        self.uri = uri
        msg = "could not resolve {!r} into a component".format(str(self.uri))
        super().__init__(description=msg, **kwds)
        return
                 

# end of file 
