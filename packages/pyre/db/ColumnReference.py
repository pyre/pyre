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


    # interface
    def onDelete(self, action):
        """
        Perform {action} when the referenced row is deleted
        """
        # record the action
        self.delete = action
        # enable chaining
        return self


    def onUpdate(self, action):
        """
        Perform {action} when the referenced column get a new value
        """
        # record the action
        self.update = action
        # enable chaining
        return self


    # meta methods
    def __init__(self, spec, **kwds):
        super().__init__(**kwds)

        try:
            self.table, self.column = spec
        except TypeError:
            self.table = spec
            self.column = None

        return

# end of file 
