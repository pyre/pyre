# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# super class
from .Column import Column


# declaration
class Primary(Column):
    """
    A selector that serves a column of primary keys, i.e. a column all of whose values are
    distinct and can be used as an index into the sheet
    """

    # meta-methods
    def __getitem__(self, value):
        """
        Retrieve the sheet row that contains {value} in my column
        """
        # get my sheet
        sheet = self.sheet
        # ask the map of my key for the row number
        row = sheet.pyre_keys[self.field].locate(key=value)
        # and return the associated record
        return sheet.pyre_data[row]


# end of file
