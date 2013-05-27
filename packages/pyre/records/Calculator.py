# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# declaration
class Calculator:
    """
    A strategy for pulling data from a stream that attaches the values to {pyre.calc} nodes,
    making the record instances mutable
    """

    # types
    from ..calc.Node import variable


    # meta-methods
    def __call__(self, record, source, **kwds):
        """
        Pull values from {source}, convert and yield them
        """
        # zip together the data stream and the descriptors
        for field, value in zip(record.pyre_fields, source):
            # build a node to hold it
            node = self.variable(value=value, converter=field.coerce)
            # and make it available
            yield node
        # all done
        return


# end of file 
