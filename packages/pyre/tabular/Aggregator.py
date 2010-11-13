# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.AttributeClassifier import AttributeClassifier


class Aggregator(AttributeClassifier):
    """
    The metaclass that builds coördinate systems for sheets
    """


    # types
    from .Dimension import Dimension


    # meta methods
    def __new__(cls, name, bases, attributes, sheet=None, **kwds):
        """
        Build a new chart class record
        """
        # adjust the attributes
        if sheet is not None:
            # make sure ancestral sheets are identical to mine
            for base in bases:
                if base.pyre_Sheet is not None and base.pyre_Sheet is not sheet:
                    raise NotImplementedError("NYI!")
            # attach the supplied sheet
            attributes["pyre_Sheet"] = sheet
        # class data
        attributes["pyre_dimensions"] = ()
        attributes["pyre_localDimensions"] = ()
        attributes["pyre_inheritedDimensions"] = ()
        # instance data
        attributes["pyre_facts"] = None
        attributes["pyre_bins"] = ()

        # build the chart record
        chart = super().__new__(cls, name, bases, attributes, **kwds)

        # harvest the locally declared dimensions
        localDimensions = tuple(cls.pyre_harvest(attributes, cls.Dimension))
        # extract the inherited dimensions
        inheritedDimensions = []
        # prime the set of known names
        known = set(attributes)
        # iterate over the ancestors of {cls}
        for base in chart.__mro__[1:]:
            # narrow the search down to subclasses of {Chart}
            if isinstance(base, cls):
                # loop over this ancestor's local dimensions
                for dimension in base.pyre_localDimensions:
                    # skip this dimension is it is shadowed
                    if dimension.name in known: continue
                    # otherwise, save it
                    inheritedDimensions.append(dimension)
            # in any case, add this ancestor's attrinutes to the list of known names
            known.update(base.__dict__)
        # convert to read-only storage
        inheritedDimensions = tuple(inheritedDimensions)
        # attach the dimesion tuples to the chart record
        chart.pyre_localDimensions = localDimensions
        chart.pyre_inheritedDimensions = inheritedDimensions
        chart.pyre_dimensions = localDimensions + inheritedDimensions

        # and return the new chart
        return chart


    def __init__(self, name, bases, attributes, sheet=None, **kwds):
        """
        Initialize a newly minted chart class
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)
        # iterate over the locally declared dimensions
        for dimension in self.pyre_localDimensions:
            # retrieve and store the record offset of the associated measure
            dimension.offset = self.pyre_Sheet.pyre_offset(dimension.measure)
        # all done
        return


# end of file 
