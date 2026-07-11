#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the exception hierarchy the bindings register has the right shape, and that a failed
call arrives in python under its own name rather than its parent's
"""


def test():
    # access the package that hosts the bindings
    import mpi

    # and the bindings themselves
    libmpi = mpi.libmpi

    # the base of everything the package raises derives from python's own {Exception}, so a
    # caller who knows nothing of mpi can still catch it
    assert issubclass(libmpi.Error, Exception)
    # a failed mpi call is an {Error}
    assert issubclass(libmpi.MPIError, libmpi.Error)
    # and so is an argument whose shape does not fit
    assert issubclass(libmpi.ShapeError, libmpi.Error)
    # but a shape error is not an mpi failure, and neither derives from the other
    assert not issubclass(libmpi.ShapeError, libmpi.MPIError)
    assert not issubclass(libmpi.MPIError, libmpi.ShapeError)

    # bring mpi up, arranging for the shutdown
    mpi.init()
    # get the world communicator straight from the bindings
    world = libmpi.world()
    # and its size
    size = world.size
    # and my rank
    rank = world.rank

    # a scatter whose root offers the wrong number of cells is refused; this needs a peer to
    # scatter to, so only attempt it when there is more than one process
    if size > 1 and rank == 0:
        # plant a flag
        refused = False
        # ask for the impossible
        try:
            # one cell too few for the processes waiting on it
            world.scatter([0] * (size - 1), 0)
        # the mismatch must arrive under its own name, not as the base {Error}
        except libmpi.ShapeError:
            refused = True
        # check that it did
        assert refused

        # and the very same failure must still be caught when the handler asks only for the base
        refused = False
        # ask again
        try:
            world.scatter([0] * (size - 1), 0)
        # a {ShapeError} is an {Error}, so this must catch it too
        except libmpi.Error:
            refused = True
        # check
        assert refused

    # the processes that did not raise must not wait for the one that did
    world.barrier()

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
