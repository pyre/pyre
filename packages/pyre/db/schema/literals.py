# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# get the nodes
from ...calc.Node import Node as node


# the rich literals
class Literal(node.literal):
    """
    A keyword of SQL that stands for a value, such as {NULL} and {DEFAULT}
    """

    # my representations
    def __str__(self):
        """
        Render me as my keyword
        """
        # easy enough
        return self.value

    def __repr__(self):
        """
        Render me as my keyword
        """
        # easy enough
        return self.value


# the constants: the absence of a value
null = Literal(value="NULL")
# and the default value of a column
default = Literal(value="DEFAULT")


# end of file
