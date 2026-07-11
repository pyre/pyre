#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the group bindings: membership, the set operations python spells as methods, the
comparisons, and the translation of ranks from one group to another
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

    # the group of every process in the world
    everyone = world.group()
    # holds them all
    assert everyone.size == size
    # in which i have my usual rank
    assert everyone.rank == rank
    # it has members, so it is not empty
    assert everyone.isEmpty() is False
    # and it names a real group, so it is not null
    assert everyone.isNull() is False
    # which makes it true in a boolean test
    assert bool(everyone) is True

    # the group of the even ranks
    evens = everyone.include([peer for peer in range(size) if peer % 2 == 0])
    # holds exactly half of them, rounding up
    assert evens.size == (size + 1) // 2

    # the group with rank zero left out
    others = everyone.exclude([0])
    # is one smaller than the world
    assert others.size == size - 1

    # the union of the two covers everybody the world holds, since between them they leave
    # nobody out
    union = evens.union(others)
    assert union.size == size

    # the intersection holds the even ranks other than zero
    intersection = evens.intersection(others)
    assert intersection.size == len([peer for peer in range(size) if peer % 2 == 0 and peer != 0])

    # the difference holds only what {evens} has and {others} does not, which is rank zero alone
    difference = evens.difference(others)
    assert difference.size == (1 if size > 0 else 0)

    # a group is identical to itself
    assert everyone.compare(everyone) == libmpi.Comparison.identical
    # a freshly built group with the same members in the same order shares its membership, so it
    # compares equal one way or the other: congruent in general, or identical when mpi hands back
    # the very same handle, as it does for a lone process
    twin = everyone.include(list(range(size)))
    assert everyone.compare(twin) in (libmpi.Comparison.identical, libmpi.Comparison.congruent)

    # the members of the even group carry ranks of their own inside it, from zero on up
    local = list(range(evens.size))
    # translating those back to the world recovers the even ranks, in order
    world_ranks = evens.translateRanks(local, everyone)
    assert world_ranks == [peer for peer in range(size) if peer % 2 == 0]

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
