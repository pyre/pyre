# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# get the bindings
from ..extensions import libh5

# if they exist
if libh5 is not None:
    # pull in the subpackages
    from . import disktypes
    from . import memtypes
    from . import schema
    from . import api

    # shortcuts
    reader = api.reader
    writer = api.writer

    # convenience
    def read(**kwds):
        """
        Ask a generic reader to read a data product
        """
        # easy enough
        return reader().read(**kwds)


# end of file
