# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


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

    # constants
    category = 'mpi'

    # user configurable state
    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'


    # framework support
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Build a package instance
        """
        # get the os distribution
        distribution = cls.pyre_host.distribution

        # the default for {macports} machines
        if distribution == 'macports':
            # is to use openmpi
            from .OpenMPI import OpenMPI as default
        # for all others, just chain up and let my superclass hunt the right package down
        else:
            default = super().pyre_default(**kwds)

        # all done
        return default


# end of file
