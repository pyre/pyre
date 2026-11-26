# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""

# superclass
from ..framework.exceptions import FrameworkError


# marker
class TabularError(FrameworkError):
    """
    The base class of all exceptions raised by this package
    """


# a key that more than one row of a sheet holds
class DuplicateKeyError(TabularError):
    """
    Exception raised when more than one row of a sheet holds the same value in a column of
    primary keys
    """

    # public data
    description = "key '{0.key}' is in more than one row of column '{0.field}' of '{0.name}'"

    # meta-methods
    def __init__(self, sheet, field, key, **kwds):
        """
        Record that more than one row of {sheet} holds {key} in the column of {field}
        """
        # chain up
        super().__init__(**kwds)
        # store the sheet
        self.sheet = sheet
        # its name
        self.name = sheet.pyre_name
        # the name of the column
        self.field = field.name
        # and the key
        self.key = key
        # all done
        return


# end of file
