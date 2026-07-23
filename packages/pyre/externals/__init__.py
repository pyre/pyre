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
    Build a trait descriptor suitable for describing the list of package categories on which
    applications depend
    """
    # get the trait descriptors
    from ..traits import properties

    # {requirements} is a list of package category names
    return properties.list(schema=properties.str(), **kwds)


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
    Resolve the {requested} package categories, including their transitive dependencies, and
    return a report with the configured installations in link order
    """
    # delegate to the index
    return index().resolve(requested=requested)


# convenience
from .Package import Package as package
from .Tool import Tool as tool
from .Library import Library as library
from .Recipe import Recipe as recipe


# the package abstractions
def blas():
    """
    The BLAS package category
    """
    # grab the protocol
    from .BLAS import BLAS as blas

    # and generate a facility
    return blas()


def cython():
    """
    The Cython package category
    """
    # grab the protocol
    from .Cython import Cython as cython

    # and generate a facility
    return cython()


def eigen():
    """
    The Eigen package category
    """
    # grab the protocol
    from .Eigen import Eigen as eigen

    # and generate a facility
    return eigen()


def fftw():
    """
    The FFTW package category
    """
    # grab the protocol
    from .FFTW import FFTW as fftw

    # and generate a facility
    return fftw()


def gcc():
    """
    The GCC package category
    """
    # grab the protocol
    from .GCC import GCC as gcc

    # and generate a facility
    return gcc()


def gsl():
    """
    The GSL package category
    """
    # grab the protocol
    from .GSL import GSL as gsl

    # and generate a facility
    return gsl()


def hdf5():
    """
    The HDF5 package category
    """
    # grab the protocol
    from .HDF5 import HDF5 as hdf5

    # and generate a facility
    return hdf5()


def metis():
    """
    The METIS package category
    """
    # grab the protocol
    from .Metis import Metis as metis

    # and generate a facility
    return metis()


def mpi():
    """
    The MPI package category
    """
    # grab the protocol
    from .MPI import MPI as mpi

    # and generate a facility
    return mpi()


def numpy():
    """
    The numpy package category
    """
    # grab the protocol
    from .NumPy import NumPy as numpy

    # and generate a facility
    return numpy()


def parmetis():
    """
    The ParMETIS package category
    """
    # grab the protocol
    from .ParMetis import ParMetis as parmetis

    # and generate a facility
    return parmetis()


def petsc():
    """
    The PETSc package category
    """
    # grab the protocol
    from .PETSc import PETSc as petsc

    # and generate a facility
    return petsc()


def postgres():
    """
    The Postgres package category
    """
    # grab the protocol
    from .Postgres import Postgres as postgres

    # and generate a facility
    return postgres()


def pybind11():
    """
    The pybind11 package category
    """
    # grab the protocol
    from .Pybind11 import Pybind11 as pybind11

    # and generate a facility
    return pybind11()


def python():
    """
    The Python package category
    """
    # grab the protocol
    from .Python import Python as python

    # and generate a facility
    return python()


def vtk():
    """
    The VTK package category
    """
    # grab the protocol
    from .VTK import VTK as vtk

    # and generate a facility
    return vtk()


# end of file
