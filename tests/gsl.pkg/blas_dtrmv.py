#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise {dtrmv}
"""


def test():
    # get the package
    import gsl

    # the vector x
    x = gsl.vector(shape=3)
    x[0], x[1], x[2] = 1, 2, 3
    # the matrix A
    A = gsl.matrix(shape=(3, 3)).identity()

    # compute the form
    y = gsl.blas.dtrmv(gsl.Triangle.upper, gsl.Transpose.transpose, gsl.Diagonal.unit, A, x.clone())

    # check
    # print(tuple(y))
    assert tuple(y) == tuple(x)

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
