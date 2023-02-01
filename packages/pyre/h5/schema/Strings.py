# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Dataset import Dataset


# a custom container
class Strings(Dataset.list):
    """
    A list of strings
    """

    # metamethods
    def __init__(self, schema=Dataset.str(name="sentinel"), **kwds):
        # chain up with the correct schema
        super().__init__(schema=schema, **kwds)
        # all done
        return


# end of file
