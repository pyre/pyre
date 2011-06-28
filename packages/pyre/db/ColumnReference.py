# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .. import schema


class ColumnReference:
    """
    A column decorator that encapsulates references to table columns
    """


    # public data
    table = None # the table class
    column = None # the column descriptor

    update = None # the specified action to take when the referenced column is updated
    delete = None # the specified action to take when the referenced column is deleted


    # meta methods
    def __init__(self, ref, onDelete=None, onUpdate=None, **kwds):
        super().__init__(**kwds)

        # record the column spec
        try:
            self.table, self.column = ref
        except TypeError:
            self.table = ref
            self.column = None

        # and the actions
        self.delete = onDelete
        self.update = onUpdate

        return

# end of file 
