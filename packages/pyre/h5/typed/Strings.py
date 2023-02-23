# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from ..schema.Dataset import Dataset


# a list of strings
class Strings(Dataset.list):
    """
    Implementation details of the dataset mixin that supports a {list} of {str}
    """

    # metamethods
    def __init__(self, **kwds):
        # set the schema and chain up
        super().__init__(schema=Dataset.str(name="sentinel"), **kwds)
        # all done
        return

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk
        """
        # read the value
        value = dataset._pyre_id.strings()
        # and return the raw contents
        return value


# end of file
