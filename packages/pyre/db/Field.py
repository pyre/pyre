# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import traits
# superclass
from .Entry import Entry


# declaration
class Field(traits.descriptor, Entry.variable):
    """
    The base class for database table descriptors

    This class is endowed with the full algebra from {pyre.algebraic} so that field
    descriptors can be used in expressions to specify constraints or fields in views
    """


    # types
    from . import actions
    from .ForeignKey import ForeignKey
    from .FieldReference import FieldReference


    # field decorations
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
        Mark a field as a primary key
        """
        # mark 
        self._primary = True
        # primary keys do not get default values
        self.default = None
        # and return
        return self


    def unique(self):
        """
        Mark a field as containing values that are unique across the table rows
        """
        # mark 
        self._unique = True
        # and return
        return self


    def notNull(self):
        """
        Mark a field as not accepting a NULL value
        """
        # mark 
        self._notNull = True
        # and return
        return self


    def references(self, **kwds):
        """
        Mark a field as a foreign key.
        """
        # use the specification to create a field reference object and record it
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
            return " DEFAULT {}".format(self.rep(self.default))
        # otherwise just send back an empty string
        return ""


    def toSQL(self, instance):
        """
        Retrieve my value from {instance} and render it in a manner suitable for an SQL statement
        """
        # get the value
        value = instance._pyre_data[self]
        # handle 'NULL'
        if value is instance.null: return 'NULL'
        # handle 'DEFAULT'
        if value is instance.default: return 'DEFAULT'
        # handle lazy assignments
        # if isinstance(value, instance.lazy): value = value.value
        # otherwise, render and return 
        return self.rep(value)


    def __get__(self, instance, cls):
        """
        Table attribute access is interpreted as a request for the pair (table, descriptor)
        """
        # at the class level
        if instance is None:
            # build a reference to this field
            return self.FieldReference(table=cls, field=self)
        # otherwise, look my value up in the instance cache
        return instance._pyre_data[self]


    # private data
    # the following markers interpret None as 'unspecified'
    _primary = None # am i a primary key?
    _unique = None # are my values unique across the rows of the table?
    _notNull = None # do i accept NULL as a value?
    _foreign = None # foreign key: a tuple (foreign_table, field_descriptor)


# end of file 
