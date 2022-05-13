#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# superclass
from pyre.patterns.AttributeClassifier import AttributeClassifier


# dataset harvester
class Schema(AttributeClassifier):
    """
    Harvest dataset descriptors from h5 groups
    """


    # my descriptor
    from .Dataset import Dataset as dataset


    # metamethods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build the class record of a new h5 group
        """
        # build the record
        group = super().__new__(cls, name, bases, attributes, **kwds)
        # and return the new class record
        return group


    def __call(self, **kwds):
        """
        Build an instance of one of my classes
        """
        # build the instance
        group = super().__call__(**kwds)
        # and return the new instance
        return group


# end of file
