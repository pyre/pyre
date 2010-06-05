# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
This packages contains the various top level framework managers.

This is the home of the pyre executive, a singleton that provides access to all pyre framework
services. Use pyre.executive() to gain access to this object. The remainder of the classes that
are defined here are not meant to be instantiated directly, unless you are trying to extend the
framework. Be aware that the framework bootstrapping process is fairly sensitive to the
instantiation and initialization order of these objects, so caveat emptor.
"""


# the framework singleton
def executive(**kwds):
    """
    Factory for the framework executive.

    The pyre executive is a singleton that builds and maintains the collection of top-level
    framework objects that provide the runtime framework services
    """
    from .Pyre import Pyre
    return Pyre(**kwds)


# factories for other managers
def newCalculator(**kwds):
    from ..config import newCalculator
    return newCalculator(**kwds)


def newCodecManager(**kwds):
    from ..codecs import newManager
    return newManager(**kwds)


def newCommandLineParser(**kwds):
    from ..config import newCommandLineParser
    return newCommandLineParser(**kwds)


def newConfigurator(**kwds):
    from ..config import newConfigurator
    return newConfigurator(**kwds)


def newBinder(**kwds):
    from .Binder import Binder
    return Binder(**kwds)


def newFileServer(**kwds):
    from .FileServer import FileServer
    return FileServer(**kwds)


def newComponentRegistrar(**kwds):
    from ..components import newRegistrar
    return newRegistrar(**kwds)


# exceptions
from .. import PyreError


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
