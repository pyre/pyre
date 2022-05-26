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


    # framework hooks
    def pyre_sync(self):
        """
        Hook invoked when the {inventory} lookup fails and a value must be generated
        """
        # this is the value you are looking for...
        return self


# end of file
