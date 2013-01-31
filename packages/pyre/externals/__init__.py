# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# convenience
from .Package import Package as package
from .Tool import Tool as tool
from .Library import Library as library


# the packages with built-in support
# N.B.: do not use the usual pattern for exporting package symbols; hide the import of the
# package managers in functions to prevent importing them prematurely. This has the important
# side-effect of making the plug-ins from user space higher priority than the built-in support

def mpi():
    """
    The package manager for MPI installations
    """
    # get the class record
    from .MPI import MPI
    # and return it
    return MPI


def python():
    """
    Package manager for the python interpreter
    """
    # get the class record
    from .Python import Python
    # and return it
    return Python


# end of file 
