# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .. import records


class Selector(records.selector):
    """
    The basic selector that provides named access to sheet columns
    """

    # types
    from .Column import Column as column  # access to the entries of a given column

    # meta-methods
    def __get__(self, sheet, cls):
        """
        Read access to the field slice from the data set
        """
        # if this is access as a class attribute
        if sheet is None:
            # return the field descriptor
            return self.field
        # otherwise, bind a column to the sheet and return it
        return self.column(sheet=sheet, field=self.field, index=self.index)


# end of file
