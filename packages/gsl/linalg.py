# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved
"""
Support for the linear algebra interface
"""

# externals
from . import libgsl as gsl
from .Matrix import Matrix
from .Permutation import Permutation


# LU
def LU_decomposition(matrix):
    """
    Compute the LU decomposition of a matrix; {matrix} is overwritten with its factors
    """
    # allocate the permutation the decomposition will fill
    p = Permutation(shape=matrix.rows)
    # decompose {matrix} in place, filling {p}, and collecting the sign of the permutation
    sign = gsl.linalg_LU_decomp(matrix, p)
    # return the triplet
    return (matrix, p, sign)


def LU_invert(matrix, permutation, sign):
    """
    Compute the inverse of {matrix} given its LU decomposition; a new matrix is returned
    """
    # allocate the matrix the inverse will fill
    inverse = Matrix(shape=matrix.shape)
    # fill it from the factors
    gsl.linalg_LU_invert(matrix, permutation, inverse)
    # and return it
    return inverse


def LU_det(matrix, permutation, sign):
    """
    Compute the determinant of {matrix} given its LU decomposition
    """
    # easy enough
    return gsl.linalg_LU_det(matrix, sign)


def LU_lndet(matrix, permutation, sign):
    """
    Compute the determinant of {matrix} given its LU decomposition
    """
    # easy enough
    return gsl.linalg_LU_lndet(matrix)


# Cholesky
def cholesky_decomposition(matrix):
    """
    Compute the Cholesky decomposition of a symmetric positive definite matrix
    """
    # compute the decomposition, in place
    gsl.linalg_cholesky_decomp(matrix)
    # and return the matrix
    return matrix


# end of file
