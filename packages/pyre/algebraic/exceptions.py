# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


from ..framework.exceptions import FrameworkError


class NodeError(FrameworkError):
    """
    Base class for pyre.algebraic errors. Useful as a catch-all
    """


class CircularReferenceError(NodeError):
    """
    Signal a circular reference in the evaluation graph
    """

    def __init__(self, node, path=(), **kwds):
        msg = "the evaluation graph has a cycle at {0.node}"
        super().__init__(description=msg, **kwds)
        self.node = node
        self.path = path
        return


# end of file
