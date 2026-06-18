# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
import nisar


# the single-look-complex datum
class SLC(nisar.h5.schema.array):
    """
    A single-look-complex datum: a two dimensional raster of complex floats at
    full resolution

    This is the fundamental SLC measurement; every polarization channel of an
    SLC product is one of these. Its extents are deliberately left open here and
    are supplied by the product's shape schema.
    """

    # construction
    def __init__(self, shape=None, **kwds):
        """
        Fix the cell type to complex and the shape to two dimensions
        """
        # an SLC is a two dimensional array of complex floats; both extents are free
        # unless a caller supplies them
        if shape is None:
            shape = [..., ...]
        # chain up
        super().__init__(schema=nisar.h5.schema.complex(), shape=shape, **kwds)
        # all done
        return


# end of file
