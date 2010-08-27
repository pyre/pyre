# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


def chain(*, this, next):
    """
    Build a locator that ties together two others in order to express that something in {next}
    caused {this} to be recorded
    """
    from .Chain import Chain
    return Chain(this, next)


def here(level=0):
    """
    Build a locator that records the caller's location

    The parameter {level} specifies the level above the caller that is to be used as the
    originating location. The default, {level}=0, indicates to use the caller's location;
    setting {level} to 1 will use the caller's caller's location, and so on.
    """
    import traceback
    source, line, function, text = traceback.extract_stack(limit=2+level)[0]
    return newScriptLocator(source=source, line=line, function=function)


def newCommandLocator(*, arg):
    """
    Build a locator that records the position of a command line argument
    """
    from .Command import Command
    return Command(arg)


def newFileLocator(*, source, line=None, column=None):
    """
    Build a locator that records a position within a file
    """

    from .File import File
    return File(source, line, column)


def newFileRegionLocator(*, start, end=None):
    """
    Build a locator that identifies a region in a file
    """

    from .FileRegion import FileRegion
    return FileRegion(start, end)


def newScriptLocator(*, source, line=None, function=None):
    """
    Build a locator that records information extracted from a python stack trace
    """

    from .Script import Script
    return Script(source, line, function)


def newSimpleLocator(*, source):
    """
    Build a simple locator that just names the given {source}
    """

    from .Simple import Simple
    return Simple(source)


def newTracker():
    """
    Build a new history tracker, an object that maintains a log of all the values a given key
    has ever assumed, along with locators that describe the location of these assignments
    """
    from .Tracker import Tracker
    return Tracker()


# end of file
