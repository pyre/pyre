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
        # all done
        return

    # value synchronization
    def pyre_pull(self):
        """
        Read my value from disk and update my cache
        """
        # read the value
        value = self.pyre_id.strings()
        # store it
        self.value = value
        # and return the raw contents
        return value


# end of file
