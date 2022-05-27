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
    def pyre_sync(self, instance, **kwds):
        """
        Hook invoked when the {inventory} lookup fails and a value must be generated
        """
        # build a clone of mine to hold my client's values for my structure
        group = type(self)(name=self.pyre_name, at=self.pyre_location)
        # attach it
        self.pyre_set(instance=instance, value=group)
        # and return it
        return group


# end of file
