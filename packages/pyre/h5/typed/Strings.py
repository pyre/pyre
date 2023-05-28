# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
from .. import libh5

# superclass
from ..schema.Dataset import Dataset


# a list of strings
class Strings(Dataset.list):
    """
    Implementation details of the dataset mixin that supports a {list} of {str}
    """

    # constants
    typename = "strings"  # the name of my type

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
        # attempt to
        try:
            # read the value
            value = dataset._pyre_id.strings()
        # if something goes wrong
        except RuntimeError as error:
            # make a channel
            channel = journal.error("pyre.h5.typed.strings")
            # report
            channel.line(f"hdf5 runtime error: {error}")
            channel.line(f"while reading a list of strings")
            channel.line(f"from {dataset}")
            # flush
            channel.log()
            # and, just in case errors aren't fatal, return an empty list
            return []

        # and return the raw contents
        return value

    def _pyre_push(self, src, dst: libh5.DataSet):
        """
        Push my cache value to disk
        """
        # grab the value
        value = src.value
        # and attempt
        try:
            # to write it out
            dst.strings(value)
        # if something goes wrong
        except RuntimeError as error:
            # make a channel
            channel = journal.error("pyre.h5.typed.strings")
            # report
            channel.line(f"hdf5 runtime error: {error}")
            channel.line(f"while writing {value}")
            channel.line(f"to {dst}")
            # and flush
            channel.log()
        # all done
        return

    # framework hooks
    def _pyre_dataspace(self, value, **kwds):
        """
        Create a diskspace instance that describes scalar types
        """
        # easy
        return libh5.DataSpace(shape=[len(value)])


# end of file
