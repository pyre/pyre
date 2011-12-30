# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class ForeignKey:
    """
    A field decorator that encapsulates references to table fields
    """

 
    # types
    from .FieldReference import FieldReference


    # public data
    update = None # the specified action to take when the referenced field is updated
    delete = None # the specified action to take when the referenced field is deleted
    reference = None # the table/field i refer to


    # meta methods
    def __init__(self, key=None, onDelete=None, onUpdate=None, **kwds):
        super().__init__(**kwds)

        # if {key} is already a field reference
        if isinstance(key, self.FieldReference):
            reference = key
        # otherwise, assume {key} is a table
        else:
            reference = self.FieldReference(table=key, field=None)

        # record the field reference
        self.reference = key
        # and the actions
        self.delete = onDelete
        self.update = onUpdate

        return


# end of file 
