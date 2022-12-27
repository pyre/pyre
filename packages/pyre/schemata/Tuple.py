# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Sequence import Sequence


# declaration
class Tuple(Sequence):
    """
    The tuple type declarator
    """

    # constants
    typename = "tuple"  # the name of my type
    container = tuple  # the container i represent


# end of file
