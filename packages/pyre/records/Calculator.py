# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Calculator:
    """
    A strategy for pulling data from a stream that attaches the values to {pyre.calc} nodes,
    making the record instances mutable
    """

    # types
    from ..calc.Node import Node as node

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
        Pull values from {source}, and yield a {pyre.calc} variable for each one that converts
        its value whenever it is read
        """
        # make {pyre.calc} variables so record fields are mutable
        variable = self.node.variable
        # zip together the data stream and the descriptors
        for field, value in zip(record.pyre_fields, source):
            # build a node to hold it
            node = variable(value=value, postprocessor=field.process)
            # and make it available
            yield node
        # all done
        return


# end of file
