#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the partitioner over the single process stand-in for a communicator

This is the path a machine with no mpi takes, where the extension has no {bcastVector} to call;
deliberately, this test never brings the mpi runtime up
"""


def test():
    # setup the workload
    parameters = 8

    # externals
    import gsl

    # build a vector, without ever touching the mpi runtime
    θ = gsl.vector(shape=parameters)
    # initialize it
    for dof in range(parameters):
        θ[dof] = dof

    # broadcasting from the lone process hands back what it already holds
    result = gsl.vector.bcast(vector=θ)
    # so the values survive
    for dof in range(parameters):
        assert result[dof] == dof

    # collecting from the lone process gathers its whole contribution
    collected = gsl.vector.collect(vector=θ)
    # into fresh storage
    assert collected is not θ
    # that carries the same values
    for dof in range(parameters):
        assert collected[dof] == dof

    # scattering among the lone process hands it the whole vector
    mine = gsl.vector(shape=parameters).excerpt(vector=θ)
    # so it gets every value
    for dof in range(parameters):
        assert mine[dof] == dof

    # a source that names a task which does not exist is an error
    try:
        # ask for a broadcast from rank one
        gsl.vector.bcast(vector=θ, source=1)
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
        gsl.vector.bcast()
    # which is what should happen
    except TypeError:
        pass
    # and if it doesn't
    else:
        # the guard is gone
        assert False, "the source must supply a vector"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
