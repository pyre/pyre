# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import itertools
from ..patterns.AttributeClassifier import AttributeClassifier


class Templater(AttributeClassifier):
    """
    Metaclass that inspects sheet declarations
    """


    # types
    from .Accessor import Accessor
    from .Measure import Measure
    from .Record import Record


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
        sheet.pyre_localMeasures = list(cls.pyre_harvest(attributes, cls.Measure))

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
        recordName = name + "_record"
        recordBases = (cls.Record, )
        recordAttributes = {
            measure.name: cls.Accessor(index=index)
            for index, measure in enumerate(sheet.pyre_measures()) 
            }
        recordAttributes["__doc__"] = "The class that specifies sheet rows"
        recordType = type(recordName, recordBases, recordAttributes)
        # attach it to the sheet
        sheet.pyre_Record = recordType

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
