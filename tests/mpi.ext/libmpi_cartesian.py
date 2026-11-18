#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the cartesian communicator bindings: arrange the processes on a grid and walk it by
    coordinates, by rank, and by stepping along an axis
    """
    # access the package that hosts the bindings
    import mpi

    # bring mpi up, arranging for the shutdown
    mpi.init()
    # get the bindings
    libmpi = mpi.libmpi
    # and the world communicator straight from them
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
        # so my predecessor is nobody
        assert behind == libmpi.procNull
    # everywhere else
    else:
        # my predecessor is one step back
        assert behind == rank - 1
    # at the high end nobody follows me
    if rank == size - 1:
        # so my successor is nobody
        assert ahead == libmpi.procNull
    # everywhere else
    else:
        # my successor is one step on
        assert ahead == rank + 1

    # keeping the only axis
    whole = line.sub(keep=[1])
    # makes another cartesian communicator
    assert isinstance(whole, libmpi.Cartesian)
    # that spans the whole grid again
    assert whole.size == size

    # dropping it
    alone = line.sub(keep=[0])
    # makes another cartesian communicator too
    assert isinstance(alone, libmpi.Cartesian)
    # that leaves each process alone on a grid of one
    assert alone.size == 1

    # a grid whose rows do not wrap but whose columns do reaches the multi-axis paths the single
    # axis above cannot, and mixes the two kinds of axis; with three rows, the middle one has
    # neighbors on both sides while the outer ones fall off the edge, and with at least three
    # columns my two neighbors along a row are distinct processes; so the grid needs a process
    # count that is a multiple of three, and at least nine
    if size >= 9 and size % 3 == 0:
        # the number of rows
        rows = 3
        # and of columns
        columns = size // rows
        # arrange the processes on the grid, wrapping only the columns, numbering held fixed
        grid = world.cartesian(axes=[rows, columns], periods=[0, 1], reorder=0)
        # the grid has two axes
        assert grid.dimensions == 2
        # of the shape we asked for
        assert grid.axes == [rows, columns]
        # and only the second one wraps
        assert grid.periods == [0, 1]

        # where my coordinate and my rank name the same spot both ways: get my coordinate
        here = grid.coordinates()
        # and look up the rank that sits there
        assert grid.rankAt(here) == grid.rank
        # unpack my place on the grid
        row, column = here
        # with the numbering fixed, the processes fill the grid one row at a time
        assert grid.rank == row * columns + column

        # stepping along the first axis names my neighbors in the rows above and below mine
        above, below = grid.shift(direction=0, displacement=1)
        # the top row has nobody above it, since the rows do not wrap
        if row == 0:
            # so my neighbor above is nobody
            assert above == libmpi.procNull
        # everywhere else
        else:
            # it is the process one row up, in my column
            assert above == grid.rankAt([row - 1, column])
        # similarly, the bottom row has nobody below it
        if row == rows - 1:
            # so my neighbor below is nobody
            assert below == libmpi.procNull
        # everywhere else
        else:
            # it is the process one row down, in my column
            assert below == grid.rankAt([row + 1, column])

        # stepping along the second axis names my neighbors in my row, which always exist since
        # the columns wrap
        left, right = grid.shift(direction=1, displacement=1)
        # the one on my left, wrapping around from the first column to the last
        assert left == grid.rankAt([row, (column - 1) % columns])
        # the one on my right, wrapping around from the last column to the first
        assert right == grid.rankAt([row, (column + 1) % columns])
        # and they are two different processes
        assert left != right

        # keeping only the first axis makes the column of the grid i belong to
        myColumn = grid.sub(keep=[1, 0])
        # which holds one process from each row
        assert myColumn.size == rows
        # and does not wrap
        assert myColumn.periods == [0]
        # keeping only the second axis makes my row
        myRow = grid.sub(keep=[0, 1])
        # which holds one process from each column
        assert myRow.size == columns
        # and wraps
        assert myRow.periods == [1]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
