# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from ..Dataset import Dataset

# a list of strings
class Strings(Dataset.list):
    """
    Implementation details of the dataset mixin that supports a {list} of {str}
    """

    # metamethods
    def __init__(self, **kwds):
        # set the schema and chain up
        super().__init__(schema=Dataset.str(name="sentinel"), **kwds)
        # initialize my shape
        self.shape = []
        # all done
        return

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Read my value from disk and update my cache
        """
        # read the value
        value = dataset._pyre_id.strings()
        # store it
        self.value = value
        # update my shape
        self.shape = dataset._pyre_id.shape
        # and return the raw contents
        return value


# end of file