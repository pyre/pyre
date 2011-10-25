# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class ForeignKey:
    """
    A column decorator that encapsulates references to table columns
    """

 
    # types
    from .ColumnReference import ColumnReference


    # public data
    update = None # the specified action to take when the referenced column is updated
    delete = None # the specified action to take when the referenced column is deleted
    reference = None # the table/column i refer to


    # meta methods
    def __init__(self, key=None, onDelete=None, onUpdate=None, **kwds):
        super().__init__(**kwds)

        # if {key} is already a column reference
        if isinstance(key, self.ColumnReference):
            reference = key
        # otherwise, assume {key} is a table
        else:
            reference = self.ColumnReference(table=key, column=None)

        # record the column reference
        self.reference = key
        # and the actions
        self.delete = onDelete
        self.update = onUpdate

        return


# end of file 
