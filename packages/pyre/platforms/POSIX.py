# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os
# superclass
from .Host import Host


# declaration
class POSIX(Host, family='pyre.platforms.posix'):
    """
    Encapsulation of a POSIX host
    """


    # public data
    platform = 'posix'
    distribution = 'unknown'
    systemdirs = ['/usr'] # canonical package installation locations


    # interface
    def which(self, filename):
        """
        Search for {filename} through the list of path prefixes in the {PATH} environment variable
        """
        # trivial after python 3.3...
        import shutil
        return shutil.which(filename)


# end of file
