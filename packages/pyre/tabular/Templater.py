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
    def __new__(cls, name, bases, attributes, hidden=False, **kwds):
        """
        Build a new worksheet record
        """
        # build the record
        sheet = super().__new__(cls, name, bases, attributes, **kwds)

        # no need to be shy here about accessing the record: there is no Templater.__setattr__
        # add the introspection attributes
        sheet.pyre_name = name

        # harvest the local measures
        if not hidden:
            sheet.pyre_localMeasures = list(cls.pyre_harvest(attributes, cls.Measure))
        else:
            sheet.pyre_localMeasures = []

        # extract the inherited measures from the superclasses
        sheet.pyre_inheritedMeasures = []
        # prime the set of known names
        known = set(attributes)
        # iterate over the ancestors of the sheet
        for base in sheet.__mro__[1:]:
            # focus on other sheets
            if isinstance(base, cls):
                # loop over its local measures
                for measure in base.pyre_localMeasures:
                    # skip it if it is shadowed by some other attributes
                    if measure.name in known: continue
                    # otherwise save it
                    sheet.pyre_inheritedMeasures.append(measure)
            # in any case, add all the attributes of this base class to the known set
            known.update(base.__dict__)

        # create the Record subclass that holds the data

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
        Build a new sheet
        """
        # create the sheet
        print("Templater.__call__: building a new sheet instance")
        sheet = super().__call__(**kwds)
        # and return it
        return sheet



# end of file 
