# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .. import schema
from .. import algebraic


class Column(schema.descriptor, algebraic.node):
    """
    The base class for database table descriptors

    This class is endowed with the full algebra from {pyre.algebraic} so that column
    descriptors can be used in expressions to specify constraints or columns in views
    """


    # types
    from . import actions
    from .ForeignKey import ForeignKey
    from .ColumnReference import ColumnReference


    # column decorations
    def setDefault(self, value):
        """
        Set a new default value
        """
        # install the new value
        self.default = value
        # enable chaining
        return self


    def primary(self):
        """
        Mark a column as a primary key
        """
        # mark 
        self._primary = True
        # primary keys do not get default values
        self.default = None
        # and return
        return self


    def unique(self):
        """
        Mark a column as containing values that are unique across the table rows
        """
        # mark 
        self._unique = True
        # and return
        return self


    def notNull(self):
        """
        Mark a column as not accepting a NULL value
        """
        # mark 
        self._notNull = True
        # and return
        return self


    def references(self, **kwds):
        """
        Mark a column as a foreign key.
        """
        # use the specification to create a column reference object and record it
        self._foreign = self.ForeignKey(**kwds)
        # and return
        return self
        

    # implementation details
    def decldefault(self):
        """
        Invoked by the SQL mill to create the default value part of the declaration
        """
        # if my default has been specified
        if self.default is not None:
            # render it
            return " DEFAULT {}".format(self.default)
        # otherwise just send back an empty string
        return ""


    def __get__(self, instance, cls):
        """
        Table attribute access is interpreted as a request for the pair (table, descriptor)
        """
        # at the class level
        if instance is None:
            # build a reference to this field
            return self.ColumnReference(table=cls, column=self)
        # otherwise, look my value up in the instance cache
        return instance._pyre_data[self]



    # private data
    # the following markers interpret None as 'unspecified'
    _primary = None # am i a primary key?
    _unique = None # are my values unique across the rows of the table?
    _notNull = None # do i accept NULL as a value?
    _foreign = None # foreign key: a tuple (foreign_table, column_descriptor)


# end of file 
