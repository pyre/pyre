# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
from nisar import h5


# the single-look-complex datum
class SLC(h5.schema.array):
    """
    A single-look-complex datum: a two dimensional raster of complex floats at
    full resolution

    This is the fundamental SLC measurement; every polarization channel of an
    SLC product is one of these. Its extents are deliberately left open here and
    are supplied by the product's shape schema.
    """

    # construction
    def __init__(self, **kwds):
        """
        Fix the cell type to complex and the rank to two
        """
        # an SLC is a rank-2 array of complex floats
        super().__init__(schema=h5.schema.complex(), rank=2, **kwds)
        # all done
        return


# end of file
