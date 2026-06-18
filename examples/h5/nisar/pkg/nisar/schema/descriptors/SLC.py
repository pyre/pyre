# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import nisar


# the single-look-complex datum
class SLC(nisar.h5.schema.array):
    """
    A single-look-complex datum: a two dimensional raster of complex floats at full
    resolution, azimuth × range

    This is the fundamental SLC measurement; every polarization channel of an SLC product is
    one of these. Its shape is intrinsic — the two named dimensions {nlines} and {nsamples},
    resolved by scope against the product's shape index at realization — so it is fixed here
    rather than offered as a constructor convenience.
    """

    # construction
    def __init__(self, **kwds):
        """
        Fix the cell type to complex and the shape to the two named SLC dimensions
        """
        # an SLC is a 2d raster of complex floats over the (nlines, nsamples) grid
        super().__init__(
            schema=nisar.h5.schema.complex(), shape=["nlines", "nsamples"], **kwds
        )
        # all done
        return


# end of file
