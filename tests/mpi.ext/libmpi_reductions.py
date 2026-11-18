#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the reduction family that the bindings spell as named methods: the whole-number and
    real-number overloads must be told apart by the argument, and naming a destination must deliver
    the answer to that rank alone
    """
    # access the package that hosts the bindings
    import mpi

    # bring mpi up, arranging for the shutdown
    mpi.init()
    # get the bindings
    libmpi = mpi.libmpi
    # and the world communicator straight from them
    world = libmpi.world()
    # and its structure: the number of processes
    size = world.size
    # and my place among them
    rank = world.rank
    # the sum of every rank, which the checks below lean on
    total = size * (size - 1) // 2

    # a sum over whole numbers is dispatched to the integral overload
    whole = world.sum(item=rank)
    # so it stays whole
    assert isinstance(whole, int)
    # and adds up
    assert whole == total

    # a sum over real numbers is dispatched to the real overload
    real = world.sum(item=float(rank))
    # so it stays real
    assert isinstance(real, float)
    # and adds up too
    assert real == float(total)

    # the max, the min, and the product, each delivered to everybody: the largest rank
    assert world.max(item=rank) == size - 1
    # the smallest
    assert world.min(item=rank) == 0
    # and the product of the ranks, which is zero once rank zero joins in
    assert world.product(item=rank) == 0

    # naming a destination delivers the answer to that rank alone
    largest = world.max(item=rank, destination=0)
    # so only the root sees it
    if rank == 0:
        # as the largest rank
        assert largest == size - 1
    # and everybody else
    else:
        # is handed nothing
        assert largest is None

    # the collectives that name their operator rather than implying it agree with the above
    assert world.allreduce(rank, libmpi.Op.sum) == total
    # and preserve the cell type in the same way
    assert isinstance(world.allreduce(float(rank), libmpi.Op.sum), float)

    # an inclusive scan hands me the sum over everybody who precedes me, myself included
    assert world.scan(rank, libmpi.Op.sum) == rank * (rank + 1) // 2

    # the exclusive one leaves me out, and the standard leaves it undefined at rank zero
    running = world.exscan(rank, libmpi.Op.sum)
    # so at rank zero
    if rank == 0:
        # there is nothing to report
        assert running is None
    # everywhere else
    else:
        # it is the sum over my strict predecessors
        assert running == rank * (rank - 1) // 2

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
