# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import shutil

# superclass
from .Host import Host

# parts
from .Tools import Tools


# declaration
class POSIX(Host, family="pyre.platforms.posix"):
    """
    Encapsulation of a POSIX host
    """

    # public data
    platform = "posix"
    distribution = "unknown"

    # user configurable state
    # the commonly available tools
    tools = Tools()

    # interface
    @classmethod
    def systemdirs(cls):
        """
        Generate a sequence of directories with system wide package installations
        """
        # the default u*ix locations
        yield "/usr"
        # and nothing else
        return

    @classmethod
    def which(cls, filename):
        """
        Search for {filename} through the list of path prefixes in the {PATH} environment variable
        """
        # trivial after python 3.3...
        return shutil.which(filename)


# end of file
