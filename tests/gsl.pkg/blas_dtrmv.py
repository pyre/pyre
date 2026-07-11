#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise {dtrmv}, pinning the {Triangle}, {Transpose}, and {Diagonal} flags to hand computed
results so a flag wired backwards is caught rather than silently accepted
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

    # the input vector
    x = gsl.vector(shape=3)
    x[0], x[1], x[2] = 1.0, 1.0, 1.0

    # the upper triangle times x: [[2,3,4],[0,6,7],[0,0,10]] . [1,1,1] = [9, 13, 10]
    upper = gsl.blas.dtrmv(
        gsl.Triangle.upper, gsl.Transpose.noTranspose, gsl.Diagonal.nonUnit, A, x.clone()
    )
    assert tuple(upper) == (9.0, 13.0, 10.0)

    # the lower triangle times x: [[2,0,0],[5,6,0],[8,9,10]] . [1,1,1] = [2, 11, 27]; a swapped
    # uplo flag would fail here
    lower = gsl.blas.dtrmv(
        gsl.Triangle.lower, gsl.Transpose.noTranspose, gsl.Diagonal.nonUnit, A, x.clone()
    )
    assert tuple(lower) == (2.0, 11.0, 27.0)

    # the transpose of the upper triangle times x: [[2,0,0],[3,6,0],[4,7,10]] . [1,1,1] = [2,9,21];
    # a swapped transpose flag would fail here
    transposed = gsl.blas.dtrmv(
        gsl.Triangle.upper, gsl.Transpose.transpose, gsl.Diagonal.nonUnit, A, x.clone()
    )
    assert tuple(transposed) == (2.0, 9.0, 21.0)

    # the upper triangle with a unit diagonal times x: [[1,3,4],[0,1,7],[0,0,1]] . [1,1,1] =
    # [8, 8, 1]; a swapped diag flag would fail here
    unit = gsl.blas.dtrmv(
        gsl.Triangle.upper, gsl.Transpose.noTranspose, gsl.Diagonal.unit, A, x.clone()
    )
    assert tuple(unit) == (8.0, 8.0, 1.0)

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
