# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

"""
This package contains the various top level framework managers.

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


# the factories of the various managers
def newBinder(**kwds):
    from .Binder import Binder
    return Binder(**kwds)


def newCodecManager(**kwds):
    from ..config import newCodecManager
    return newCodecManager(**kwds)


def newCommandLineParser(**kwds):
    from ..config import newCommandLineParser
    return newCommandLineParser(**kwds)


def newComponentRegistrar(**kwds):
    from ..components import newRegistar
    return newRegistar(**kwds)


def newConfigurator(**kwds):
    from ..config import newConfigurator
    return newConfigurator(**kwds)


def newFileServer(**kwds):
    from .FileServer import FileServer
    return FileServer(**kwds)


def newTimerRegistrar(**kwds):
    from ..timers import newTimerRegistrar
    return newTimerRegistrar(**kwds)


# end of file 
