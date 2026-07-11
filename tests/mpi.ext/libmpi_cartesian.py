#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the cartesian communicator bindings: arrange the processes on a grid and walk it by
coordinates, by rank, and by stepping along an axis
"""


def test():
    # access the package that hosts the bindings
    import mpi

    # bring mpi up, arranging for the shutdown
    mpi.init()
    # get the world communicator straight from the bindings
    libmpi = mpi.libmpi
    world = libmpi.world()
    # and its size
    size = world.size

    # lay every process out on a single, non-wrapping axis; hold the numbering fixed so that a
    # process keeps the rank it had in the world, and its coordinate is exactly that rank
    line = world.cartesian(axes=[size], periods=[0], reorder=0)
    # my rank within the grid
    rank = line.rank

    # the grid has one axis
    assert line.dimensions == 1
    # whose extent is the process count
    assert line.axes == [size]
    # which does not wrap
    assert line.periods == [0]

    # with the numbering fixed, i sit at the coordinate that matches my rank
    assert line.coordinates() == [rank]
    # asking about a named rank agrees
    assert line.coordinates(rank) == [rank]
    # and the inverse recovers the rank that sits at a coordinate
    assert line.rankAt([rank]) == rank

    # stepping one place along the axis names my two neighbors: the one that would send to me,
    # and the one i would send to
    behind, ahead = line.shift(direction=0, displacement=1)
    # at the low end nobody precedes me, so the axis does not wrap and the walk falls off
    if rank == 0:
        assert behind == libmpi.procNull
    # everywhere else my predecessor is one step back
    else:
        assert behind == rank - 1
    # at the high end nobody follows me
    if rank == size - 1:
        assert ahead == libmpi.procNull
    # everywhere else my successor is one step on
    else:
        assert ahead == rank + 1

    # keeping the only axis spans the whole grid again
    whole = line.sub(keep=[1])
    assert isinstance(whole, libmpi.Cartesian)
    assert whole.size == size

    # dropping it leaves each process alone on a grid of one
    alone = line.sub(keep=[0])
    assert isinstance(alone, libmpi.Cartesian)
    assert alone.size == 1

    # when the process count is an even number greater than one, a two by half grid exercises the
    # multi-axis paths the single axis above cannot reach
    if size > 1 and size % 2 == 0:
        # arrange the processes on two rows, wrapping the second axis, numbering held fixed
        grid = world.cartesian(axes=[2, size // 2], periods=[1, 1], reorder=0)
        # the grid has two axes
        assert grid.dimensions == 2
        # of the shape we asked for
        assert grid.axes == [2, size // 2]
        # where my coordinate and my rank name the same spot both ways
        here = grid.coordinates()
        assert grid.rankAt(here) == grid.rank

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
