# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# my superclass
from .Node import Node


# declaration
class Ignorable(Node):
    """
    Handler that ignores the subtree anchored at its tag
    """

    # interface
    def newNode(self, **kwds):
        """
        Invoked when a new opening tag is encountered in my subtree
        """
        # just return myself
        return self

    def newQNode(self, **kwds):
        """
        Invoked when a new namespace qualified opening tag is encountered in my subtree
        """
        # just return myself
        return self

    def notify(self, **kwds):
        """
        Invoked when a closing tag in encountered in my subtree
        """
        return

    # meta methods
    def __init__(self, **kwds):
        return


# end of file
