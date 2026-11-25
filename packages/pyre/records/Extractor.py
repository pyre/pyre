# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Extractor:
    """
    A strategy for pulling data from a stream and performing value coercions indicated by the
    field descriptors
    """

    # interface
    def arity(self, record) -> int:
        """
        The number of values a row of {record} holds: one for each of its fields
        """
        # easy enough
        return len(record.pyre_fields)

    # meta-methods
    def __call__(self, record, source, **kwds):
        """
        Pull values from {source}, convert and yield them
        """
        # zip together the data stream and the descriptors
        for field, value in zip(record.pyre_fields, source):
            # convert the value
            value = field.process(value)
            # and make it available
            yield value
        # all done
        return


# end of file
