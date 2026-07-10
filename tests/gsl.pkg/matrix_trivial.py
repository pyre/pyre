#!/usr/bin/env python3
# -*- Python -*-
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
    # setup the workload
    rows = 4
    columns = 2

    # externals
    import gsl

    # build a matrix, without ever touching the mpi runtime
    θ = gsl.matrix(shape=(rows, columns))
    # initialize it
    for row in range(rows):
        for column in range(columns):
            θ[row, column] = row * columns + column

    # broadcasting from the lone process hands back what it already holds
    result = gsl.matrix.bcast(matrix=θ)
    # so the values survive
    for row in range(rows):
        for column in range(columns):
            assert result[row, column] == row * columns + column

    # collecting from the lone process gathers its whole contribution
    collected = gsl.matrix.collect(matrix=θ)
    # into fresh storage
    assert collected is not θ
    # that carries the same values
    for row in range(rows):
        for column in range(columns):
            assert collected[row, column] == row * columns + column

    # scattering among the lone process hands it the whole matrix
    mine = gsl.matrix(shape=(rows, columns)).excerpt(matrix=θ)
    # so it gets every value
    for row in range(rows):
        for column in range(columns):
            assert mine[row, column] == row * columns + column

    # a source that names a task which does not exist is an error
    try:
        # ask for a broadcast from rank one
        gsl.matrix.bcast(matrix=θ, source=1)
    # which is what should happen
    except ValueError:
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
