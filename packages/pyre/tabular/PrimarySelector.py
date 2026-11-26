# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Selector import Selector


class PrimarySelector(Selector):
    """
    The selector that provides named access to a column of primary keys
    """

    # types
    from .Primary import Primary as primary  # access to an indexed column

    # meta-methods
    def __get__(self, sheet, cls):
        """
        Read access to the column of primary keys
        """
        # if this is access as a class attribute
        if sheet is None:
            # return the field descriptor
            return self.field
        # otherwise, make an indexed column over the sheet and return it
        return self.primary(sheet=sheet, field=self.field, index=self.index)


# end of file
