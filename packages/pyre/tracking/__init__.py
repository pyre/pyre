# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


def newTracker():
    from .Tracker import Tracker
    return Tracker()


def chain(*, this, next):
    from .Chain import Chain
    return Chain(this, next)


def newFileLocator(*, source, line=None, column=None):
    """
    Build a new File locator
    """

    from .File import File
    return File(source, line, column)


def newFileRegionLocator(*, start, end=None):
    """
    Build a new File locator
    """

    from .FileRegion import FileRegion
    return FileRegion(start, end)


def newScriptLocator(*, source, line=None, function=None):
    """
    Build a new Script locator
    """

    from .Script import Script
    return Script(source, line, function)


def newSimpleLocator(*, source):
    """
    Build a new Simple locator
    """

    from .Simple import Simple
    return Simple(source)


# end of file 
