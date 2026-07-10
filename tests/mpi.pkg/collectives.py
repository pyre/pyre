#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the collective family, each of which names its operator explicitly
"""


def test():
    # access the package
    import mpi

    # initialize
    mpi.init()
    # get the world communicator
    world = mpi.world
    # and its structure
    size = world.size
    rank = world.rank
    # the sum of every rank, which several of the checks below lean on
    total = size * (size - 1) // 2

    # a reduction over whole numbers stays whole
    assert isinstance(world.allreduce(rank, mpi.Op.sum), int)
    # and adds up
    assert world.allreduce(rank, mpi.Op.sum) == total
    # a reduction over real numbers stays real
    assert isinstance(world.allreduce(float(rank), mpi.Op.sum), float)
    # and adds up too
    assert world.allreduce(float(rank), mpi.Op.sum) == float(total)

    # the extrema
    assert world.allreduce(rank, mpi.Op.maximum) == size - 1
    assert world.allreduce(rank, mpi.Op.minimum) == 0

    # a reduction that names a destination delivers to that rank alone
    largest = world.reduce(rank, mpi.Op.maximum, 0)
    # so only the root sees an answer
    if rank == 0:
        assert largest == size - 1
    # and everybody else is told there is none
    else:
        assert largest is None

    # an inclusive scan hands me the sum over everybody who precedes me, myself included
    assert world.scan(rank, mpi.Op.sum) == rank * (rank + 1) // 2

    # the exclusive one leaves me out
    running = world.exscan(rank, mpi.Op.sum)
    # and the standard leaves it undefined at rank zero, where nothing precedes
    if rank == 0:
        assert running is None
    # everywhere else it is the sum over my strict predecessors
    else:
        assert running == rank * (rank - 1) // 2

    # gather every rank at the root
    gathered = world.gather(rank, 0)
    # only the root collects
    if rank == 0:
        assert gathered == list(range(size))
    # and everybody else is told so
    else:
        assert gathered is None

    # the same, delivered to everybody
    assert world.allgather(rank) == list(range(size))

    # scatter one cell per process from the root; only the root's cells matter
    parcels = [2 * slot for slot in range(size)] if rank == 0 else []
    # each process receives the cell addressed to it
    assert world.scatter(parcels, 0) == 2 * rank

    # every process hands one cell to every process, each carrying its own rank
    assert world.alltoall([rank] * size) == list(range(size))

    # the object collectives carry whatever pickle can flatten, so the contribution of each
    # process is a different type and a different size
    mine = {"rank": rank, "payload": "x" * (rank + 1)}

    # collect them all at the root
    collected = world.gatherObject(mine, 0)
    # only the root collects
    if rank == 0:
        # one object per process, in rank order
        assert collected == [{"rank": slot, "payload": "x" * (slot + 1)} for slot in range(size)]
    # and everybody else is told so
    else:
        assert collected is None

    # the same, delivered to everybody
    everyone = world.allgatherObject(mine)
    # one object per process
    assert len(everyone) == size
    # the last of which carries the longest payload
    assert everyone[size - 1] == {"rank": size - 1, "payload": "x" * size}

    # hand an object of a different type and size to each process; only the root's matter
    bundles = [("rank", slot) * (slot + 1) for slot in range(size)] if rank == 0 else None
    # each process receives the one addressed to it
    assert world.scatterObject(bundles, 0) == ("rank", rank) * (rank + 1)

    # every process hands one object to every process, and says who packed it. the payload
    # leans on the sender twice as heavily as on the receiver, so that what i address to {peer}
    # is a different size from what {peer} addresses to me
    deliveries = [{"from": rank, "pad": "y" * (2 * rank + peer)} for peer in range(size)]
    # exchange
    received = world.alltoallObject(deliveries)
    # so i receive one object from each process, in rank order, sized as its sender decided
    assert received == [{"from": peer, "pad": "y" * (2 * peer + rank)} for peer in range(size)]

    # an exchange in which somebody brought the wrong number of objects is refused; every
    # process refuses, so nobody is left waiting
    if size > 1:
        # plant a flag
        refused = False
        # ask for the impossible
        try:
            # one object too few
            world.alltoallObject([None] * (size - 1))
        # the package refuses with a shape error
        except mpi.ShapeError:
            refused = True
        # check that it did
        assert refused

    # a scatter whose root brought the wrong number of objects is refused, exactly as the cell
    # version is
    if rank == 0 and size > 1:
        # plant a flag
        refused = False
        # ask for the impossible
        try:
            # one object too few
            world.scatterObject([None] * (size - 1), 0)
        # the package refuses with a shape error
        except mpi.ShapeError:
            refused = True
        # check that it did
        assert refused

    # the ranks that did not raise must not wait for the one that did
    world.barrier()

    # a scatter whose root brought the wrong number of cells is refused
    if rank == 0 and size > 1:
        # plant a flag
        refused = False
        # ask for the impossible
        try:
            # one cell too few
            world.scatter([0] * (size - 1), 0)
        # the package refuses with a shape error
        except mpi.ShapeError:
            refused = True
        # check that it did
        assert refused

    # the ranks that did not raise must not wait for the one that did
    world.barrier()

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
