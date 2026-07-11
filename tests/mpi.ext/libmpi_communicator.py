#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the communicator bindings: its structure, its comparisons, and the factories that carve
new communicators, groups, ports, and grids out of it
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

    # a real communicator is true and not null
    assert bool(world) is True
    assert world.isNull() is False

    # the set of processes it holds is a group of the same size, in which i have the same rank
    group = world.group()
    assert group.size == size
    assert group.rank == rank

    # a communicator is identical to itself
    assert world.compare(world) == libmpi.Comparison.identical

    # a duplicate has my membership but a fresh context, so it is a genuine communicator
    twin = world.duplicate()
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
        assert lone is not None
        assert lone.size == 1
    # and everybody else is left out, and told so
    else:
        assert lone is None

    # excluding rank zero builds the complement
    rest = world.exclude([0])
    # which rank zero is not part of
    if rank == 0:
        assert rest is None
    # while everybody else lands in a communicator one smaller than the world
    else:
        assert rest is not None
        assert rest.size == size - 1

    # restricting to my whole group hands everybody a communicator congruent to me
    full = world.restrict(world.group())
    assert full is not None
    assert full.size == size

    # a port to a peer is a genuine conduit
    conduit = world.port(peer=rank, tag=3)
    assert isinstance(conduit, libmpi.Port)
    # that remembers the peer and the label
    assert conduit.peer == rank
    assert conduit.tag == 3

    # laying my processes out on a one dimensional grid hands back a cartesian communicator
    grid = world.cartesian(axes=[size], periods=[0])
    assert isinstance(grid, libmpi.Cartesian)
    # which, being a communicator, still knows how many processes it holds
    assert grid.size == size

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
