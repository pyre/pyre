# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# superclass
from .MPI import MPI


# the mpich package manager
class MPICH(MPI, family='pyre.externals.mpich'):
    """
    The package manager for MPICH packages
    """


# end of file
