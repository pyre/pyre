#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the partitioner over the single process stand-in for a communicator

This is the path a machine with no mpi takes, where the extension has no {bcastMatrix} to call;
deliberately, this test never brings the mpi runtime up
"""


def test():
    # setup the workload: the number of rows
    rows = 4
    # and columns
    columns = 2

    # externals
    import gsl

    # build a matrix, without ever touching the mpi runtime
    θ = gsl.matrix(shape=(rows, columns))
    # initialize it: go through its rows
    for row in range(rows):
        # and its columns
        for column in range(columns):
            # and number the cells in row major order
            θ[row, column] = row * columns + column

    # broadcasting from the lone process hands back what it already holds
    result = gsl.matrix.bcast(matrix=θ)
    # so the values survive: go through the rows
    for row in range(rows):
        # and the columns
        for column in range(columns):
            # and check each cell
            assert result[row, column] == row * columns + column

    # collecting from the lone process gathers its whole contribution
    collected = gsl.matrix.collect(matrix=θ)
    # into fresh storage
    assert collected is not θ
    # that carries the same values: go through the rows
    for row in range(rows):
        # and the columns
        for column in range(columns):
            # and check each cell
            assert collected[row, column] == row * columns + column

    # scattering among the lone process hands it the whole matrix
    mine = gsl.matrix(shape=(rows, columns)).excerpt(matrix=θ)
    # so it gets every value: go through the rows
    for row in range(rows):
        # and the columns
        for column in range(columns):
            # and check each cell
            assert mine[row, column] == row * columns + column

    # a source that names a task which does not exist is an error
    try:
        # ask for a broadcast from rank one
        gsl.matrix.bcast(matrix=θ, source=1)
    # which is what should happen
    except ValueError:
        # so there is nothing else to check
        pass
    # and if it doesn't
    else:
        # the guard is gone
        assert False, "a source of rank one should not be reachable"

    # neither may the source arrive empty handed
    try:
        # ask for a broadcast of nothing at all
        gsl.matrix.bcast()
    # which is what should happen
    except TypeError:
        # so there is nothing else to check
        pass
    # and if it doesn't
    else:
        # the guard is gone
        assert False, "the source must supply a matrix"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
