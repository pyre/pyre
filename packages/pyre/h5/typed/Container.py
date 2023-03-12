# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the mixin for containers
class Container:
    """
    The base class for all container types
    """

    # metamethods
    def __init__(self, schema, **kwds):
        # extract my {memtype} and {disktype} from my {schema}
        memtype = schema.memtype
        disktype = schema.disktype
        # chain up
        super().__init__(schema=schema, memtype=memtype, disktype=disktype, **kwds)
        # all done
        return


# end of file
