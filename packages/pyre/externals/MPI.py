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
        Identify the default implementation of MPI
        """
        # get the host
        host = cls.pyre_host
        # attempt to
        try:
            # dispatch to my host specific handlers
            package = host.identify(authority=cls)
        # if something goes wrong
        except AttributeError:
            # use a generic mpich as the default
            from .MPICH import MPICH as package
        # and return it
        return package


    @classmethod
    def macports(cls, host):
        """
        Identify the default implementation of MPI on macports machines
        """
        # this is a macports host; ask it for the selected mpi package
        selection, alternatives = host.selected(cls.category)
        # if the selection is an openmpi variant
        if selection.startswith('openmpi'):
            # get the support for OpenMPI
            from .OpenMPI import OpenMPI
            # and return it
            return OpenMPI

        # if the selection is an mpich variant
        if selection.startswith('mpich'):
            # get the support for MPICH
            from .MPICH import MPICH
            # and return it
            return MPICH

        # anything else is an error
        raise cls.ExternalNotFoundError(category=cls.category)


# end of file
