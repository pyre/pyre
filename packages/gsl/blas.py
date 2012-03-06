# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#
"""
Support for the BLAS interface
"""

# externals
from . import gsl


# the interface for doubles
# level 1
def ddot(x, y):
    """
    Compute the scalar product {x^T y}
    """
    # compute and return the result
    return gsl.blas_ddot(x.data, y.data)


def dnrm2(x):
    """
    Compute the Euclidean norm
    """
    # compute and return the result
    return gsl.blas_dnrm2(x.data)


def dasum(x):
    """
    Compute the sum of the absolute values of the entries in {x}
    """
    # compute and return the result
    return gsl.blas_dasum(x.data)


def daxpy(α, x, y):
    """
    Compute {α x + y} and store the result in {y}
    """
    # compute
    gsl.blas_daxpy(α, x.data, y.data)
    # and return the result {y}
    return y


# level 2
def dsymv(uplo, α, A, x, β, y):
    """
    Compute {y = α A x + β y}
    """
    # compute
    gsl.blas_dsymv(uplo, α, A.data, x.data, β, y.data)
    # and return the result in {y}
    return y


def dsyr(uplo, α, x, A):
    """
    Compute {A = α x x^T + A}
    """
    # compute
    gsl.blas_dsyr(uplo, α, x.data, A.data)
    # and return the result in {A}
    return A


# end of file 
