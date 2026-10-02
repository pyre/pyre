# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# factories
from .Chain import Chain as chain
from .Command import Command as command
from .File import File as file
from .FileRegion import FileRegion as region
from .NameLookup import NameLookup as lookup
from .Script import Script as script
from .Simple import Simple as simple
from .Tracker import Tracker as tracker

# constants
# the stack depth of the caller relative to {traceback.extract_stack}, taking into account the
# frame added by {pyre} itself
callerStackDepth = 2


# in case we just don't know
def unknown():
    return simple(source="<unknown>")


# dynamic locators
def here(level=0):
    """
    Build a locator that records the caller's location

    The parameter {level} specifies the level above the caller that is to be used as the
    originating location. The default, {level}=0, indicates to use the caller's location;
    setting {level} to 1 will use the caller's caller's location, and so on.
    """
    # externals
    import sys

    # get the frame of the requested caller, which is all a locator needs; a stack trace would
    # also read the text of every line in it from the source files, which is never used
    frame = sys._getframe(callerStackDepth + level - 1)
    # get its code
    code = frame.f_code
    # hand its location to the script locator
    return script(source=code.co_filename, line=frame.f_lineno, function=code.co_name)


# end of file
