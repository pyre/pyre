# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.AttributeClassifier import AttributeClassifier


class Templater(AttributeClassifier):
    """
    Metaclass that inspects sheet declarations
    """


    # types
    from .Measure import Measure


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build a new worksheet record
        """
        # harvest the measures
        measures = cls.pyre_harvest(attributes, cls.Measure)
        print(measures)
        # build the record
        sheet = super().__new__(cls, name, bases, attributes, descriptors="pyre_measures", **kwds)
        # return the class record
        return sheet


    def __init__(self, name, bases, attributes, **kwds):
        """
        Initialize a newly minted worksheet class
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)
        # and return
        return


    def __call__(self, **kwds):
        """
        Build a new row
        """
        # create the row
        row = super().__call__(**kwds)
        # and return it
        return row



# end of file 
