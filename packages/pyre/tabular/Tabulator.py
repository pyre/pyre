# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .. import records


# declaration
class Tabulator(records.templater):
    """
    Metaclass that builds sheets
    """

    # types
    from .Selector import Selector as pyre_selector  # override the one in {records}
    from .PrimarySelector import PrimarySelector as pyre_primarySelector  # for primary keys

    # meta-methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build a new worksheet
        """
        # prime the name attribute; instances are given names by the user
        attributes["pyre_name"] = name
        # build the record
        sheet = super().__new__(cls, name, bases, attributes, **kwds)
        # return the class record
        return sheet

    def __init__(self, name, bases, attributes, **kwds):
        """
        Give the columns of my primary keys the selectors that index them
        """
        # chain up to attach a selector to each of my columns
        super().__init__(name, bases, attributes, **kwds)
        # go through my measures
        for measure in self.pyre_measures:
            # the ones that are not primary keys
            if not measure._primary:
                # keep their plain selectors
                continue
            # find the column of this key
            index = self.pyre_columns[measure]
            # build a selector that indexes the sheet by its values
            selector = self.pyre_primarySelector(field=measure, index=index)
            # and attach it in place of the plain one
            setattr(self, measure.name, selector)
        # all done
        return


# end of file
