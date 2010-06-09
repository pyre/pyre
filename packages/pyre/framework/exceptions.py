# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


from ..exceptions import PyreError


class FrameworkError(PyreError):
    """
    Base class for all pyre exceptions

    Useful when you are trying to catch any and all pyre framework errors
    """


class BadResourceLocatorError(FrameworkError):
    """
    Exception raised when a URI is not formed properly
    """


    def __init__(self, uri, reason, **kwds):
        super().__init__(**kwds)
        self.uri = uri
        self.reason = reason
        return


    def __str__(self):
        return "{0.uri}: {0.reason}".format(self)


# end of file 
