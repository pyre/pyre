# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# metaclass
from . import calculator


# declaration of the base node
class Node(metaclass=calculator):
    """
    The base class for lazily evaluated nodes
    """

    # not much to do


# end of file
