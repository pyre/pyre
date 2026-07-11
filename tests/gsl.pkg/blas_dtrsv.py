#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise {dtrsv}, pinning the {Triangle}, {Transpose}, and {Diagonal} flags: {dtrsv} solves
op(A) y = b, so feeding it the products {dtrmv} forms from the same flags must recover x
"""


def test():
    # get the package
    import gsl

    # a matrix whose upper and lower triangles differ
    A = gsl.matrix(shape=(3, 3))
    for i in range(3):
        for j in range(3):
            A[i, j] = float(3 * i + j + 2)
    # so A is [[2, 3, 4], [5, 6, 7], [8, 9, 10]]

    # the vector each solve must recover
    x = gsl.vector(shape=3)
    x[0], x[1], x[2] = 1.0, 1.0, 1.0

    # each flag combination paired with the product {dtrmv} forms from it and x; these products are
    # pinned to hand computed values in {blas_dtrmv}, so recovering x pins {dtrsv}'s flags to match
    cases = [
        (gsl.Triangle.upper, gsl.Transpose.noTranspose, gsl.Diagonal.nonUnit, (9.0, 13.0, 10.0)),
        (gsl.Triangle.lower, gsl.Transpose.noTranspose, gsl.Diagonal.nonUnit, (2.0, 11.0, 27.0)),
        (gsl.Triangle.upper, gsl.Transpose.transpose, gsl.Diagonal.nonUnit, (2.0, 9.0, 21.0)),
        (gsl.Triangle.upper, gsl.Transpose.noTranspose, gsl.Diagonal.unit, (8.0, 8.0, 1.0)),
    ]
    # walk the cases
    for triangle, transpose, diagonal, product in cases:
        # load the product
        b = gsl.vector(shape=3)
        b[0], b[1], b[2] = product
        # solve op(A) y = b
        y = gsl.blas.dtrsv(triangle, transpose, diagonal, A, b)
        # which must be x, to within rounding
        assert all(abs(y[i] - x[i]) < 1e-12 for i in range(3))

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
