# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import primitives

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
    def read(uri: primitives.uri, mode: str = "r", **kwds):
        """
        Ask a generic reader to read a data product
        """
        # easy enough
        return reader(uri=uri, mode=mode).read(**kwds)

    def write(uri: primitives.uri, mode: str = "w", **kwds):
        """
        Ask a generic reader to read a data product
        """
        # easy enough
        return writer(uri=uri, mode=mode).write(**kwds)


# end of file
