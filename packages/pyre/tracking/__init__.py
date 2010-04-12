# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


def newTracker():
    """
    Build a new history tracker, an object that maintains a log of all the values a given key
    has ever assumed, along with locators that describe the location of these assignments
    """
    from .Tracker import Tracker
    return Tracker()


def chain(*, this, next):
    """
    Build a locator that ties together two others in order to express that something in {next}
    caused {this} to be recorded
    """
    from .Chain import Chain
    return Chain(this, next)


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


# end of file 
