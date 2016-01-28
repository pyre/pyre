# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# my superclass
from .Launcher import Launcher


# declaration
class Slurm(Launcher, family='mpi.shells.slurm'):
    """
    Encapsulation of launching an MPI job using SLURM
    """


# end of file
