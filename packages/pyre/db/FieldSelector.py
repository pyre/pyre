# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .. import records


# declaration
class FieldSelector(records.selector):
    """
    Access to the field descriptors
    """


    # types
    from .FieldReference import FieldReference as fieldReference


    # meta-methods
    def __get__(self, record, cls):
        """
        Field retrieval
        """
        # if the target of this access is the table class, return a field reference
        if record is None: return self.fieldReference(table=cls, field=self.field)
        # otherwise, complain
        raise NotImplementedError('field selectors do not support read access to instances')


# end of file 
