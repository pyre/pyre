#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the single process stand-in for a communicator

This is what {mpi.world} names before anybody calls {mpi.init}, and everywhere on a machine
with no mpi at all; deliberately, this test never brings the runtime up
"""


def test():
    # externals
    import mpi

    # before {init}, the world is the trivial communicator
    world = mpi.world

    # it holds this process alone
    assert world.rank == 0
    assert world.size == 1
    # and it always names a communicator
    assert world.isNull is False
    assert bool(world) is True

    # the barrier is satisfied by the lone process arriving at it
    world.barrier()

    # every collective is an identity
    assert world.bcast(item=42) == 42
    assert world.reduce(item=42, op=None) == 42
    assert world.allreduce(item=42, op=None) == 42
    assert world.scan(item=42, op=None) == 42
    # except the exclusive scan, which mpi leaves undefined at rank zero
    assert world.exscan(item=42, op=None) is None

    # collecting one cell from each process yields the one cell there is
    assert world.gather(item=7) == [7]
    assert world.allgather(item=7) == [7]
    # and handing one cell to each process hands it right back
    assert world.scatter(items=[5]) == 5
    assert world.alltoall(items=[9]) == [9]

    # the object flavored collectives behave the same, on payloads that are not numbers
    assert world.gatherObject(item={"a": 1}) == [{"a": 1}]
    assert world.allgatherObject(item={"a": 1}) == [{"a": 1}]
    assert world.scatterObject(items=[{"b": 2}]) == {"b": 2}
    assert world.alltoallObject(items=[{"c": 3}]) == [{"c": 3}]

    # a duplicate holds the same lone process
    assert world.duplicate().size == 1

    # naming a rank that does not exist is an error, rather than a quietly wrong answer
    try:
        # ask for a broadcast from a task that is not there
        world.bcast(item=1, source=1)
    # which is what should happen
    except ValueError:
        pass
    # and if it doesn't
    else:
        # the guard is gone
        assert False, "a source of rank one should not be reachable"

    # so is bringing the wrong number of cells to a scatter
    try:
        # hand out two cells among one process
        world.scatter(items=[1, 2])
    # which is what should happen
    except ValueError:
        pass
    # and if it doesn't
    else:
        # the guard is gone
        assert False, "scattering two cells among one process should not be possible"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
