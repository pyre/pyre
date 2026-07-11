#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the collectives that move data rather than combine it: the number versions, which cross
the binding as lists, and the object versions, which pickle whatever they are handed
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

    # gather every rank at the root, where a c++ vector of cells crosses the binding as a list
    gathered = world.gather(rank, 0)
    # only the root collects
    if rank == 0:
        assert gathered == list(range(size))
    # and everybody else is told so
    else:
        assert gathered is None

    # the same, delivered to everybody
    assert world.allgather(rank) == list(range(size))

    # scatter one cell per process from the root; only the root's list matters
    parcels = [2 * slot for slot in range(size)] if rank == 0 else []
    # each process receives the cell addressed to it
    assert world.scatter(parcels, 0) == 2 * rank

    # every process hands one cell to every process, each carrying its own rank
    assert world.alltoall([rank] * size) == list(range(size))

    # broadcast an object from rank zero; only the source supplies one, and everybody rebuilds it
    word = world.bcast({"greeting": "hello", "from": 0} if rank == 0 else None, 0)
    assert word == {"greeting": "hello", "from": 0}

    # the object collectives carry whatever pickle can flatten, so each process brings a value of
    # a different type and a different size
    mine = {"rank": rank, "payload": "x" * (rank + 1)}

    # collect them all at the root
    collected = world.gatherObject(mine, 0)
    # only the root collects
    if rank == 0:
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

    # every process hands one object to every process, sized as its sender decided
    deliveries = [{"from": rank, "pad": "y" * (2 * rank + peer)} for peer in range(size)]
    # exchange
    received = world.alltoallObject(deliveries)
    # so i receive one object from each process, in rank order
    assert received == [{"from": peer, "pad": "y" * (2 * peer + rank)} for peer in range(size)]

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
