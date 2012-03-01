#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Access matrices by rows and columns
"""


def test():
    # package access
    import gsl
    # make a matrix
    m = gsl.matrix(shape=(100,50))
    # fill it with random values
    m.random(pdf=gsl.pdf.gaussian(sigma=2, rng=gsl.rng()))

    # rows
    i = 3
    # set the ith row to all {i}
    for j in range(m.columns) : m[i,j] = i
    # get the row using the interface
    row = m.getRow(i)
    # check that it is a vector
    assert row.shape == m.columns
    # full of {i}
    assert row == gsl.vector(shape=m.columns).fill(i)

    # columns
    j = 2
    # set the jth column to all {j}
    for i in range(m.rows): m[i,j] = j
    # get the column using the interface
    column = m.getColumn(j)
    # check that it is a vector
    assert column.shape == m.rows
    # full of {j}
    assert column == gsl.vector(shape=m.rows).fill(j)

    # all done
    return m


# main
if __name__ == "__main__":
    test()


# end of file 
