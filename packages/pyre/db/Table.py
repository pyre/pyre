# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# metaclass
from .Schemer import Schemer


# declaration
class Table(metaclass=Schemer):
    """
    Base class for database table declarations
    """


    # publicly accessible data in the protected pyre namespace
    pyre_name = None # the name of the table; must match the name in the database
    pyre_alias = None # an alias for this table; used by queries
    pyre_localFields = None # a tuple of the field descriptors that were declared locally
    pyre_fields = None # a tuple of all the field descriptors, including inherited ones


    # interface
    # declaration decorators
    @classmethod
    def pyre_primaryKey(cls, reference):
        """
        Add {reference} to the tuple of fields that must be marked as primary keys
        """
        # add it to the pile
        cls._pyre_primaryKeys.add(reference.field)
        # and return
        return cls


    @classmethod
    def pyre_unique(cls, reference):
        """
        Add {reference} to the tuple of fields that must be marked as unique
        """
        # add it to the pile
        cls._pyre_uniqueFields.add(reference.field)
        # and return
        return cls


    @classmethod
    def pyre_foreignKey(cls, field, foreign):
        """
        Mark {field} as a reference to {foreign}
        """
        # add an entry to the foreign key list
        cls._pyre_foreignKeys.append( (field, foreign) )
        # and return
        return cls


    @classmethod
    def pyre_check(cls, expression):
        """
        Add {expression} to the list of my nameless constraints
        """
        # add {expression} to my pile of constraints
        cls._pyre_constraints.append(expression)
        # and return
        return cls


    # representations
    def pyre_toSQL(self):
        """
        SQL compliant representation of my values in declaration order
        """
        return ", ".join(field.toSQL(self) for field in self.pyre_fields)


    # meta methods
    def __init__(self, **kwds):
        # build the per instance field cache
        self._pyre_data = cache ={}
        # and populate it by hunting down a value for each field
        for field in self.pyre_fields:
            # if this field is among the {kwds}
            try:
                # get the value we were passed
                value = kwds[field.name]
            # otherwise
            except KeyError:
                # look up the default
                value = field.default
            # and set it
            cache[field] = value
        # all done
        return


    # private data
    _pyre_data = None # a dictionary that holds the per-instance field values

    # these are sensitive to inheritance among tables; they may not work as expected (or at
    # all...), for the time being
    _pyre_primaryKeys = set() # the list of my primary key specifications
    _pyre_uniqueFields = set() # the list of my unique fields
    _pyre_foreignKeys = [] # the list of my foreign key specifications
    _pyre_constraints = [] # the list of my nameless constraints


# end of file 
