#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# superclass
from .Object import Object


# a dataset container
class Group(Object):
    """
    A container of datasets
    """

    # metamethods
    def __str__(self):
        """
        Human readable description
        """
        return "a group"


# end of file
