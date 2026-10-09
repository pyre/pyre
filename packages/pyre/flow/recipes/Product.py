# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Node import Node


# the products of a recipe
class Product(Node):
    """
    A product of a recipe: the specification it was declared with, if any, and its pin; the
    slots bound to it say more about what it holds
    """

    # public data
    @property
    def specification(self):
        """
        The specification i was declared with, or nothing when only my bindings decide
        """
        # it is my protocol
        return self.protocol


# end of file
