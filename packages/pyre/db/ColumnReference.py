# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .. import algebraic


class ColumnReference(algebraic.node):
    """
    A column decorator that encapsulates references to table columns

    This class is endowed with the full algebra from {pyre.algebraic} in order to support
    expressions involving table columns. Such expressions can be used to formulate constraints
    or to specify columns in views
    """


    # public data
    table = None # the table class
    column = None # the column descriptor


    # interface
    def project(self, table):
        """
        Build a reference to {table} that points to the same column as i do
        """
        return ColumnReference(table=table, column=self.column)


    # meta methods
    def __init__(self, table, column, **kwds):
        super().__init__(**kwds)

        self.table = table
        self.column = column

        return


    def __str__(self):
        """
        Convert the column reference to an expression
        """
        # if i am bound to a specific column
        if self.column is not None:
            # include its name in the generated expression
            return "{0.table.pyre_name}.{0.column.name}".format(self)
        # otherwise, just refer to the table
        return "{0.table.pyre_name}".format(self)


# end of file 
