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
    def __init__(self, schema=None, **kwds):
        # if the user didn't pick
        if schema is None:
            # make a reasonable choice
            schema = Dataset.str(name="sentinel")
        # set the schema and chain up
        super().__init__(schema=schema, **kwds)
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

    def _pyre_push(self, src, dest):
        """
        Push my cache value to disk
        """
        # grab the value
        value = src.value
        # and write it out
        dest._pyre_id.strings(value)
        # all done
        return


# end of file
