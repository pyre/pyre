# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# the marker of component factories
from .. import foundry
# the protocol for external packages
from .Category import Category as category


# a trait descriptor suitable for collecting package categories and instance specifications
def catalog(**kwds):
    """
    Build a trait descriptor suitable for building a database of available external packages
    for each package category
    """
    # get the trait descriptors
    from ..traits import properties
    # a catalog is a dictionary mapping package categories to list of packages
    return properties.catalog(schema=category(), **kwds)


def dependencies(**kwds):
    """
    Build a trait descriptor suitable for building a database of external package choices for
    each package category
    """
    # get the trait descriptors
    from ..traits import properties
    # {dependencies} is a dictionary mapping package categories to package instances
    return properties.dict(schema=category(), **kwds)


def requirements(**kwds):
    """
    Build a trait descriptor suitable for describing the list of package categories on which
    applications depend
    """
    # get the trait descriptors
    from ..traits import properties
    # {requirements} is a list of package category names
    return properties.list(schema=properties.str(), **kwds)


# convenience
from .Package import Package as package
from .Tool import Tool as tool
from .Library import Library as library


# the packages with built-in support
# N.B.: do not use the usual pattern for exporting package symbols; hide the import of the
# package managers in functions to prevent importing them prematurely. This has the important
# side-effect of making the plug-ins from user space higher priority than the built-in support


@foundry(implements=category)
def mpi():
    """
    The package manager for MPI installations
    """
    # get the class record
    from .MPI import MPI
    # and return it
    return MPI


@foundry(implements=category)
def mpich():
    """
    The package manager for MPICH installations
    """
    # get the class record
    from .MPICH import MPICH
    # and return it
    return MPICH


@foundry(implements=category)
def openmpi():
    """
    The package manager for OpenMPI installations
    """
    # get the class record
    from .OpenMPI import OpenMPI
    # and return it
    return OpenMPI


@foundry(implements=category)
def python():
    """
    Package manager for the python interpreter
    """
    # get the class record
    from .Python import Python
    # and return it
    return Python


# end of file
