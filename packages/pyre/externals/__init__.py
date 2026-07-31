# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# a trait descriptor suitable for collecting package categories and instance specifications
def catalog(**kwds):
    """
    Build a trait descriptor suitable for building a database of available external packages
    for each package category
    """
    # get the trait descriptors
    from ..traits import properties

    # a catalog is a dictionary mapping package categories to list of packages
    return properties.catalog(schema=package(), **kwds)


def dependencies(**kwds):
    """
    Build a trait descriptor suitable for building a database of external package choices for
    each package category
    """
    # get the trait descriptors
    from ..traits import properties

    # {dependencies} is a dictionary mapping package categories to package instances
    return properties.dict(schema=package(), **kwds)


def requirements(**kwds):
    """
    Build a trait descriptor suitable for describing the list of package requirements on
    which applications depend
    """
    # get the descriptor
    from .Requirements import Requirements

    # {requirements} is a list of structured requirements, coerced from text specifications
    return Requirements(**kwds)


# access to the index of external packages
def index():
    """
    Grant access to the index that manages package discovery on this host
    """
    # get the class
    from .Index import Index

    # and delegate to the singleton accessor
    return Index.index()


def resolve(requested):
    """
    Resolve the {requested} package requirements, including their transitive dependencies,
    and return a report with the configured installations in link order
    """
    # delegate to the index
    return index().resolve(requested=requested)


# convenience
from .Package import Package as package
from .Tool import Tool as tool
from .Library import Library as library
from .Recipe import Recipe as recipe
from .Requirement import Requirement as requirement


# the package abstractions
def blas(**kwds):
    """
    The BLAS package category
    """
    # grab the protocol
    from .BLAS import BLAS as blas

    # and generate a facility
    return blas(**kwds)


def cython(**kwds):
    """
    The Cython package category
    """
    # grab the protocol
    from .Cython import Cython as cython

    # and generate a facility
    return cython(**kwds)


def eigen(**kwds):
    """
    The Eigen package category
    """
    # grab the protocol
    from .Eigen import Eigen as eigen

    # and generate a facility
    return eigen(**kwds)


def fftw(**kwds):
    """
    The FFTW package category
    """
    # grab the protocol
    from .FFTW import FFTW as fftw

    # and generate a facility
    return fftw(**kwds)


def gcc(**kwds):
    """
    The GCC package category
    """
    # grab the protocol
    from .GCC import GCC as gcc

    # and generate a facility
    return gcc(**kwds)


def gsl(**kwds):
    """
    The GSL package category
    """
    # grab the protocol
    from .GSL import GSL as gsl

    # and generate a facility
    return gsl(**kwds)


def hdf5(**kwds):
    """
    The HDF5 package category
    """
    # grab the protocol
    from .HDF5 import HDF5 as hdf5

    # and generate a facility
    return hdf5(**kwds)


def metis(**kwds):
    """
    The METIS package category
    """
    # grab the protocol
    from .Metis import Metis as metis

    # and generate a facility
    return metis(**kwds)


def mpi(**kwds):
    """
    The MPI package category
    """
    # grab the protocol
    from .MPI import MPI as mpi

    # and generate a facility
    return mpi(**kwds)


def numpy(**kwds):
    """
    The numpy package category
    """
    # grab the protocol
    from .NumPy import NumPy as numpy

    # and generate a facility
    return numpy(**kwds)


def parmetis(**kwds):
    """
    The ParMETIS package category
    """
    # grab the protocol
    from .ParMetis import ParMetis as parmetis

    # and generate a facility
    return parmetis(**kwds)


def petsc(**kwds):
    """
    The PETSc package category
    """
    # grab the protocol
    from .PETSc import PETSc as petsc

    # and generate a facility
    return petsc(**kwds)


def postgres(**kwds):
    """
    The Postgres package category
    """
    # grab the protocol
    from .Postgres import Postgres as postgres

    # and generate a facility
    return postgres(**kwds)


def pybind11(**kwds):
    """
    The pybind11 package category
    """
    # grab the protocol
    from .Pybind11 import Pybind11 as pybind11

    # and generate a facility
    return pybind11(**kwds)


def python(**kwds):
    """
    The Python package category
    """
    # grab the protocol
    from .Python import Python as python

    # and generate a facility
    return python(**kwds)


def vtk(**kwds):
    """
    The VTK package category
    """
    # grab the protocol
    from .VTK import VTK as vtk

    # and generate a facility
    return vtk(**kwds)


# end of file
