#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the reduction family that the bindings spell as named methods: the whole-number and
real-number overloads must be told apart by the argument, and naming a destination must deliver
the answer to that rank alone
"""


def test():
    # access the package that hosts the bindings
    import mpi

    # bring mpi up, arranging for the shutdown
    mpi.init()
    # get the world communicator straight from the bindings
    libmpi = mpi.libmpi
    world = libmpi.world()
    # and its structure
    size = world.size
    rank = world.rank
    # the sum of every rank, which the checks below lean on
    total = size * (size - 1) // 2

    # a sum over whole numbers is dispatched to the integral overload, so it stays whole
    whole = world.sum(item=rank)
    assert isinstance(whole, int)
    # and adds up
    assert whole == total

    # a sum over real numbers is dispatched to the real overload, so it stays real
    real = world.sum(item=float(rank))
    assert isinstance(real, float)
    # and adds up too
    assert real == float(total)

    # the product, the max, and the min, each delivered to everybody
    assert world.max(item=rank) == size - 1
    assert world.min(item=rank) == 0
    # the product of the ranks is zero once rank zero joins in
    assert world.product(item=rank) == 0

    # naming a destination delivers the answer to that rank alone
    largest = world.max(item=rank, destination=0)
    # so only the root sees it
    if rank == 0:
        assert largest == size - 1
    # and everybody else is handed nothing
    else:
        assert largest is None

    # the collectives that name their operator rather than implying it agree with the above
    assert world.allreduce(rank, libmpi.Op.sum) == total
    # and preserve the cell type in the same way
    assert isinstance(world.allreduce(float(rank), libmpi.Op.sum), float)

    # an inclusive scan hands me the sum over everybody who precedes me, myself included
    assert world.scan(rank, libmpi.Op.sum) == rank * (rank + 1) // 2

    # the exclusive one leaves me out, and the standard leaves it undefined at rank zero
    running = world.exscan(rank, libmpi.Op.sum)
    if rank == 0:
        assert running is None
    # everywhere else it is the sum over my strict predecessors
    else:
        assert running == rank * (rank - 1) // 2

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
