# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Multi-dimensional arrays over pluggable memory.

A grid pairs a packing strategy, which maps a multi-dimensional index to an offset in memory,
with a storage strategy, which decides where the cells live. The C++ library carries the full
family of both; this package fronts the {libpyre} bindings, which collapse every grid to a
single class.

The sequence

    import pyre
    g = pyre.grid.heap(shape=(2, 3, 4), cell="float64")
    g[1, 2, 3] = 4.0
    x = g[1, 2, 3]

makes a grid over a fresh block of heap memory and reaches its cells by index: a full index
reads or writes one cell, while a partial or sliced index returns a sub-grid over the same
memory. A grid also presents the buffer protocol, so a consumer that speaks it reaches the cells
directly, with no copy. The grid keeps its cells alive for as long as any view or sub-grid holds
on, so {g} may go out of scope while one of them is still in use.
"""

# pull in pyre so we can reach the bindings
import pyre

# the grid bindings are the engine; a grid is a block of typed memory, so there is no sensible
# pure python stand-in for it
if pyre.libpyre is None:
    # without the bindings there is nothing to publish
    grid = None
    heap = None
    map = None
    view = None
# otherwise reach into the bindings by attribute, the way the rest of pyre does
else:
    # the type-erased grid class, for type checks
    grid = pyre.libpyre.grid.Grid
    # the factory that allocates a grid over a fresh block of heap memory
    heap = pyre.libpyre.grid.heap
    # the factory that creates a grid over a fresh memory-mapped file
    map = pyre.libpyre.grid.map
    # the factory that lays a grid over memory python already holds, without copying
    view = pyre.libpyre.grid.view


# end of file
