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
    @classmethod
    def create(cls, datastore):
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
    def drop(cls, datastore):
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


# end of file 
