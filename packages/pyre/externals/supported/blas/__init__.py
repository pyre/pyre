# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# publish the protocol
from .BLAS import BLAS as protocol

# and the implementations
from .Default import Default
from .OpenBLAS import OpenBLAS
from .Atlas import Atlas
from .GSLCBLAS import GSLCBLAS


# end of file
