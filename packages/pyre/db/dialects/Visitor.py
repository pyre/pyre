# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the local exceptions
from .. import exceptions


# declaration
class Visitor:
    """
    The base of the visitors that a dialect uses to render the columns of a table and their values
    """

    # public data
    @property
    def dialect(self):
        """
        The name of the language, for the explanations of refusals
        """
        # my mill knows
        return self.mill.dialect

    # meta-methods
    def __init__(self, mill, **kwds):
        # chain up
        super().__init__(**kwds)
        # the mill i work for
        self.mill = mill
        # all done
        return

    # implementation details
    def _refusal(self, contents, table=None, column=None, **kwds):
        """
        Build the exception that refuses {column} of {table}, or a conversion when there is no
        column, whose {contents} the language has no type for
        """
        # a column of a table
        if column is not None:
            # is named, along with its table
            subject = f"the column {table.pyre_name}.{column.name} holds {contents}"
            # and so are the objects at fault
            tableName, columnName = table.pyre_name, column.name
        # otherwise
        else:
            # it is a conversion
            subject = f"a cast to {contents}"
            # which is about no table or column
            tableName, columnName = "", ""
        # say what is wrong
        return exceptions.NotSupportedError(
            diagnostic=f"{subject}, which {self.dialect} has no type for",
            table=tableName,
            column=columnName,
        )


# end of file
