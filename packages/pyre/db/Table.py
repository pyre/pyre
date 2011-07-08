# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# metaclass
from .Schemer import Schemer


# declaration
class Table(metaclass=Schemer):
    """
    Base class for database table declarations
    """


    # constants
    from . import actions # the action markers


    # publicly accessible data in the protected pyre namespace
    pyre_name = None # the name of the table; must match the name in the database
    pyre_localColumns = None # a tuple of the column descriptors that were declared locally
    pyre_columns = None # a tuple of all the column descriptors, including inherited ones


    # interface
    # declaration decorators
    @classmethod
    def pyre_primaryKey(cls, reference):
        """
        Add {reference} to the tuple of columns that must be marked as primary keys
        """
        # add it to the pile
        cls._pyre_primaryKeys.add(reference.column)
        # and return
        return cls


    @classmethod
    def pyre_unique(cls, reference):
        """
        Add {reference} to the tuple of columns that must be marked as unique
        """
        # add it to the pile
        cls._pyre_uniqueColumns.add(reference.column)
        # and return
        return cls


    @classmethod
    def pyre_foreignKey(cls, column, foreign):
        """
        Mark {column} as a reference to {foreign}
        """
        # add an entry to the foreign key list
        cls._pyre_foreignKeys.append( (column, foreign) )
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


    # interface used by the weavers and db back-ends
    @classmethod
    def pyre_create(cls, datastore):
        """
        Convert the table specification into the appropriate SQL statements and execute them to
        create this table
        """
        # get the weaver attached to this datastore
        weaver = datastore.sql
        # generate the statements
        sql = weaver.createTable(cls)
        # and get them executed
        return datastore.execute(sql)


    @classmethod
    def pyre_drop(cls, datastore):
        """
        Convert the table specification into the appropriate SQL statements and execute them to
        remove this table from the datastore
        """
        # get the weaver attached to this datastore
        weaver = datastore.sql
        # generate the statements
        sql = weaver.dropTable(cls)
        # and get them executed
        return datastore.execute(sql)


    # private data
    # these are sensitive to inheritance among tables may not work as expected (or at all...)
    # for the time being
    _pyre_primaryKeys = set() # the list of my primary key specifications
    _pyre_uniqueColumns = set() # the list of my unique columns
    _pyre_foreignKeys = [] # the list of my foreign key specifications
    _pyre_constraints = [] # the list of my nameless constraints


# end of file 
