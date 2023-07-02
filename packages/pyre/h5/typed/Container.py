# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# access the bindings
from .. import libh5


# the mixin for containers
class Container:
    """
    The base class for all container types
    """

    # metamethods
    def __init__(self, schema, shape=None, **kwds):
        # extract my {memtype} and {disktype} from my {schema} and chain up
        super().__init__(
            schema=schema, memtype=schema.memtype, disktype=schema.disktype, **kwds
        )
        # save the shape
        self.shape = shape
        # all done
        return


# end of file
