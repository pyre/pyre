# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .. import schema


class Column(schema.descriptor):
    """
    The base class for database table descriptors
    """


    # types
    from . import actions
    from .ColumnReference import ColumnReference as referenceSpec


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
        # leave a clue for the weaver
        self._decorated = True
        # and return
        return self


    def unique(self):
        """
        Mark a column as containing values that are unique across the table rows
        """
        # mark 
        self._unique = True
        # leave a clue for the weaver
        self._decorated = True
        # and return
        return self


    def notNull(self):
        """
        Mark a column not accepting a NULL value
        """
        # mark 
        self._notNull = True
        # leave a clue for the weaver
        self._decorated = True
        # and return
        return self


    def references(self, spec):
        """
        Mark a column as a foreign key.

        Note: this call returns a {ColumnReference} instance, not a {Column} instance. Hence,
        it breaks the update chain for column descriptors and creates a chain on the reference
        spec itself.
        """
        # use the specification to create a column reference object
        foreignKey = self.referenceSpec(spec)
        # record it
        self._foreign = foreignKey
        # leave a clue for the weaver
        self._decorated = True
        # and return the reference spec
        return foreignKey
        


    # implementation details
    def decldefault(self):
        """
        Invoked by the SQL mill to create the default value part of the declaration
        """
        # if my default has been specified
        if self.default is not None:
            # render it
            return "DEFAULT {}".format(self.default)
        # otherwise just send back an empty string
        return ""


    def __get__(self, instance, cls):
        """
        Table attribute access is interpreted as a request for the pair (table, descriptor)
        """
        return (cls, self)


    # private data
    # the following markers interpret None as 'unspecified'
    _primary = None # am i a primary key?
    _unique = None # are my values unique across the rows of the table?
    _notNull = None # do i accept NULL as a value?

    _foreign = None # foreign key: a tuple (foreign_table, column_descriptor)

    _decorated = False # true when this column has decorations other than type


# end of file 
