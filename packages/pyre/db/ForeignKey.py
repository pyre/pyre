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
    column = None # the column i refer to
    update = None # the specified action to take when the referenced column is updated
    delete = None # the specified action to take when the referenced column is deleted


    # meta methods
    def __init__(self, ref=None, onDelete=None, onUpdate=None, **kwds):
        super().__init__(**kwds)

        # if {ref} is already a column reference
        if isinstance(ref, self.ColumnReference):
            reference = ref
        # otherwise, assume {ref} is a table
        else:
            reference = self.ColumnReference(table=ref, column=None)

        # record the column reference
        self.reference = reference
        # and the actions
        self.delete = onDelete
        self.update = onUpdate

        return


# end of file 
