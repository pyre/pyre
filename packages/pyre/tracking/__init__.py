# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# factories
from .Chain import Chain as chain
from .Command import Command as command
from .File import File as file
from .FileRegion import FileRegion as region
from .NameLookup import NameLookup as lookup
from .Script import Script as script
from .Simple import Simple as simple
from .Tracker import Tracker as tracker


# in case we just don't know
def unknown():
    return simple(source='<unknown>')


# dynamic locators
def here(level=0):
    """
    Build a locator that records the caller's location

    The parameter {level} specifies the level above the caller that is to be used as the
    originating location. The default, {level}=0, indicates to use the caller's location;
    setting {level} to 1 will use the caller's caller's location, and so on.
    """
    # externals
    import traceback
    # get a stack trace
    trace = traceback.extract_stack(limit=callerStackDepth+level)
    # grab the information from the current frame
    source, line, function, text = trace[0]
    # hand to the script locator
    return script(source=source, line=line, function=function)


def computeCallerStackDepth():
    """
    Compute the stack depth offset to get to the caller of a function
    """
    # at one point, i though that python 3.5 placed an extra level on the stack frame; however,
    # it doesn't seem to be the case, so we are back to treating all versions in the same
    # way. i have left the previous version of the code untouched, just in case...
    return 2

    # this is how the code stood from revno 2327 to 2521

    # the depth of the stack to the caller of {log} depends on the version of python
    import sys
    # so get the version
    major, minor, _, _, _ = sys.version_info
    # for 3.5
    if major == 3 and minor >= 5:
        # drop 3 levels
        return 3
    # for 3.4 and below
    if major == 3 and minor <= 4:
        # drop 2 levels
        return 2

    # now what
    raise NotImplementedError("unsupported python version {}.{}".format(major,minor))


# constants
callerStackDepth = computeCallerStackDepth()


# end of file
