# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
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
        # render the error message
        reason = self.description.format(self)
        # if we have a locator
        if self.locator:
            # give it a chance to pinpoint the error
            return "{.locator}: {}".format(self, reason)
        # otherwise
        return reason


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
        super().__init__(description="{0.uri}: {0.reason}", **kwds)
        self.uri = uri
        self.reason = reason
        return


class ComponentNotFoundError(FrameworkError):

    def __init__(self, uri, **kwds):
        super().__init__(description="could not resolve {0.uri} into a component", **kwds)
        self.uri = uri
        return
                 

class ExternalNotFoundError(FrameworkError):
    """
    Base class for parsing errors
    """

    def __init__(self, category, **kwds):
        msg = "could not locate support for external package {0.category!r}"
        super().__init__(description=msg, **kwds)
        self.category = category
        return


# end of file 
