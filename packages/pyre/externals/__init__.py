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


def verify(requested):
    """
    Resolve the {requested} package requirements and re-prove the markers of every
    installation against its effective configuration; return the audit
    """
    # get the index
    catalog = index()
    # resolve the request
    report = catalog.resolve(requested=requested)
    # and audit the outcome
    return catalog.verify(report=report)


# convenience
from .Package import Package as package
from .Tool import Tool as tool
from .Library import Library as library
from .Recipe import Recipe as recipe
from .Proof import Proof as proof
from .Audit import Audit as audit
from .Requirement import Requirement as requirement


# the package abstractions
def blas(**kwds):
    """
    The BLAS package category
    """
    # grab the protocol
    from .supported.blas import protocol

    # and generate a facility
    return protocol(**kwds)


def cuda(**kwds):
    """
    The CUDA package category
    """
    # grab the protocol
    from .supported.cuda import protocol

    # and generate a facility
    return protocol(**kwds)


def cython(**kwds):
    """
    The Cython package category
    """
    # grab the protocol
    from .supported.cython import protocol

    # and generate a facility
    return protocol(**kwds)


def eigen(**kwds):
    """
    The Eigen package category
    """
    # grab the protocol
    from .supported.eigen import protocol

    # and generate a facility
    return protocol(**kwds)


def fftw(**kwds):
    """
    The FFTW package category
    """
    # grab the protocol
    from .supported.fftw import protocol

    # and generate a facility
    return protocol(**kwds)


def gcc(**kwds):
    """
    The GCC package category
    """
    # grab the protocol
    from .supported.gcc import protocol

    # and generate a facility
    return protocol(**kwds)


def gsl(**kwds):
    """
    The GSL package category
    """
    # grab the protocol
    from .supported.gsl import protocol

    # and generate a facility
    return protocol(**kwds)


def hdf5(**kwds):
    """
    The HDF5 package category
    """
    # grab the protocol
    from .supported.hdf5 import protocol

    # and generate a facility
    return protocol(**kwds)


def metis(**kwds):
    """
    The METIS package category
    """
    # grab the protocol
    from .supported.metis import protocol

    # and generate a facility
    return protocol(**kwds)


def mkl(**kwds):
    """
    The MKL package category
    """
    # grab the protocol
    from .supported.mkl import protocol

    # and generate a facility
    return protocol(**kwds)


def mpi(**kwds):
    """
    The MPI package category
    """
    # grab the protocol
    from .supported.mpi import protocol

    # and generate a facility
    return protocol(**kwds)


def numpy(**kwds):
    """
    The numpy package category
    """
    # grab the protocol
    from .supported.numpy import protocol

    # and generate a facility
    return protocol(**kwds)


def parmetis(**kwds):
    """
    The ParMETIS package category
    """
    # grab the protocol
    from .supported.parmetis import protocol

    # and generate a facility
    return protocol(**kwds)


def petsc(**kwds):
    """
    The PETSc package category
    """
    # grab the protocol
    from .supported.petsc import protocol

    # and generate a facility
    return protocol(**kwds)


def postgres(**kwds):
    """
    The Postgres package category
    """
    # grab the protocol
    from .supported.postgresql import protocol

    # and generate a facility
    return protocol(**kwds)


def pybind11(**kwds):
    """
    The pybind11 package category
    """
    # grab the protocol
    from .supported.pybind11 import protocol

    # and generate a facility
    return protocol(**kwds)


def python(**kwds):
    """
    The Python package category
    """
    # grab the protocol
    from .supported.python import protocol

    # and generate a facility
    return protocol(**kwds)


def vtk(**kwds):
    """
    The VTK package category
    """
    # grab the protocol
    from .supported.vtk import protocol

    # and generate a facility
    return protocol(**kwds)


# end of file
