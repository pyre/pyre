# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Verbatim:
    """
    The strategy that builds a row out of the columns a server sent

    Every field of a selection, derived or not, is one of its columns, so the row takes one value
    per field, as it is: the server computed the derivations, and turned each value into its type
    """

    # meta-methods
    def __call__(self, record, source, **kwds):
        """
        Pull one value from {source} for each field of {record}, and yield it as it is
        """
        # go through the fields and the columns together
        for _, value in zip(record.pyre_fields, source):
            # and hand each value over
            yield value
        # all done
        return


# end of file
