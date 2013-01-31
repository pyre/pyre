# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import os
# access to the framework
import pyre
# superclass
from .Tool import Tool
from .Library import Library


# the mpi package manager
class MPI(Tool, Library, family='pyre.externals.mpi'):
    """
    The package manager for MPI packages
    """


    # user configurable state
    mpirun = pyre.properties.str() # the name of the launcher


    # public data
    category = 'mpi'

    @property
    def launcher(self):
        """
        Return the full path to the launcher
        """
        # get the name of the launcher
        launcher = self.mpirun if self.mpirun else 'mpirun'
        # join this to my binary directory and return it
        return os.path.join(self.binaries, launcher)


    # default package factory
    @classmethod
    def configureDefaultPackage(cls, package, platform):
        """
        Configure the default MPI package on the given {platform}
        """
        # localize
        mpi = package

        # if this instance did not end up getting a home directory
        if not mpi.home:
            # set it using the default system directory
            mpi.home = platform.systemdirs[0]

        # on macports
        if not mpi.mpirun and platform.distribution == 'macports':
            # adjust the name of the launcher
            mpi.mpirun = 'openmpirun'

        # all done
        return mpi


# end of file 
