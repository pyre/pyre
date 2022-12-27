# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Sequence import Sequence


# declaration
class List(Sequence):
    """
    The list type declarator
    """

    # constants
    typename = "list"  # the name of my type
    container = list  # the container i represent


# end of file
