# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
from . import libgsl as gsl

# superclass
from .Matrix import Matrix


# declaration
class MatrixView(Matrix):
    """
    A view into the data of another matrix

    A view borrows its parent's storage rather than owning any of its own, so it must not
    outlive the parent; the extension ties the two together for exactly as long as the view is
    around, so there is nothing to remember here
    """

    # meta-methods
    def __init__(self, matrix, start, shape, **kwds):
        # build the view through the extension's view constructor, bypassing the allocation my
        # superclass would otherwise do; the parent is kept alive for me automatically
        gsl.Matrix.__init__(
            self, matrix=matrix, start=tuple(map(int, start)), shape=tuple(map(int, shape)), **kwds
        )
        # all done
        return


# end of file
