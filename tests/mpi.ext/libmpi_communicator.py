#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the communicator bindings: its structure, its comparisons, and the factories that carve
    new communicators, groups, ports, and grids out of it
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

    # a real communicator is true
    assert bool(world) is True
    # and not null
    assert world.isNull() is False

    # the set of processes it holds is a group
    group = world.group()
    # of the same size
    assert group.size == size
    # in which i have the same rank
    assert group.rank == rank

    # a communicator is identical to itself
    assert world.compare(world) == libmpi.Comparison.identical

    # a duplicate has my membership but a fresh context
    twin = world.duplicate()
    # so it is a genuine communicator
    assert isinstance(twin, libmpi.Communicator)
    # with the same members in the same order, but a handle of its own: congruent, not identical
    assert world.compare(twin) == libmpi.Comparison.congruent

    # splitting by parity lands me in the communicator of my color
    mine = world.split(rank % 2)
    # which is a real communicator, since every color here is valid
    assert isinstance(mine, libmpi.Communicator)
    # and it holds every process of my parity
    assert mine.size == len([peer for peer in range(size) if peer % 2 == rank % 2])

    # including a single rank builds a communicator only that rank belongs to
    lone = world.include([0])
    # so rank zero gets a communicator of one
    if rank == 0:
        # it is there
        assert lone is not None
        # and holds rank zero alone
        assert lone.size == 1
    # and everybody else is left out
    else:
        # and told so
        assert lone is None

    # excluding rank zero builds the complement
    rest = world.exclude([0])
    # which rank zero is not part of
    if rank == 0:
        # so it gets nothing
        assert rest is None
    # while everybody else
    else:
        # lands in a communicator
        assert rest is not None
        # one smaller than the world
        assert rest.size == size - 1

    # restricting to my whole group hands everybody a communicator congruent to me
    full = world.restrict(world.group())
    # it is there
    assert full is not None
    # and holds every process
    assert full.size == size

    # a port to a peer
    conduit = world.port(peer=rank, tag=3)
    # is a genuine conduit
    assert isinstance(conduit, libmpi.Port)
    # that remembers the peer
    assert conduit.peer == rank
    # and the label
    assert conduit.tag == 3

    # laying my processes out on a one dimensional grid
    grid = world.cartesian(axes=[size], periods=[0])
    # hands back a cartesian communicator
    assert isinstance(grid, libmpi.Cartesian)
    # which, being a communicator, still knows how many processes it holds
    assert grid.size == size

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
