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
    dialect = None  # the name of the language, for the explanations of refusals

    # implementation details
    def _refusal(self, table, column, contents):
        """
        Build the exception that refuses {column} of {table}, whose {contents} the language has
        no type for
        """
        # say what is wrong, and name the table and the column
        return exceptions.NotSupportedError(
            diagnostic=(
                f"the column {table.pyre_name}.{column.name} holds {contents}, "
                f"which {self.dialect} has no type for"
            ),
            table=table.pyre_name,
            column=column.name,
        )


# end of file
