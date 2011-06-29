# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class ColumnReference:
    """
    A column decorator that encapsulates references to table columns
    """


    # public data
    table = None # the table class
    column = None # the column descriptor


    # meta methods
    def __init__(self, table, column, **kwds):
        super().__init__(**kwds)

        self.table = table
        self.column = column

        return


# end of file 
