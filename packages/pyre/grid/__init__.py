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
single class that presents the Python buffer protocol.

The sequence

    import pyre
    import numpy
    g = pyre.grid.heap(shape=(2, 3, 4), dtype="float64")
    a = numpy.asarray(g)

makes a grid over a fresh block of heap memory and views its cells with numpy, without copying:
writes through {a} land in the grid's memory. A grid presents the buffer protocol, so any
consumer of that protocol reaches its cells directly; numpy is the common one. The grid keeps
its cells alive for as long as the view holds on, so {g} may go out of scope while {a} is still
in use.
"""


# pull in pyre so we can reach the bindings
import pyre


# the grid bindings are the engine; a grid is a block of typed memory, so there is no sensible
# pure python stand-in for it
if pyre.libpyre is None:
    # without the bindings there is nothing to publish
    grid = None
    heap = None
# otherwise reach into the bindings by attribute, the way the rest of pyre does
else:
    # the erased grid class, for type checks
    grid = pyre.libpyre.grid.Grid

    # the factory that allocates a grid over a fresh block of heap memory
    heap = pyre.libpyre.grid.heap


# end of file
