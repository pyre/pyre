# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# the base class that triggers descriptor sniffing
from ..patterns.AttributeClassifier import AttributeClassifier


# declaration
class Schemer(AttributeClassifier):
    """
    Metaclass that inspects a table declaration and builds the information necessary to connect
    its attributes to the columns of the underlying table in the database back end
    """


    # types
    from .Column import Column


    # meta methods
    def __new__(cls, name, bases, attributes, id=None, **kwds):
        # chain to my ancestor
        table = super().__new__(cls, name, bases, attributes, **kwds)

        # set up the table name
        table.pyre_name = name if id is None else id
        # harvest the locally declared columns
        local = []
        for columnName, column in cls.pyre_harvest(attributes, cls.Column):
            # attach the table to the column
            column.table = table
            # set the name of the column
            column.name = columnName
            # add it to the pile
            local.append(column)
        # store the harvested columns
        table.pyre_localColumns = tuple(local)

        # now that the class record is built, we can hunt down inherited columns
        inherited = []
        # traverse the mro
        for base in reversed(table.__mro__[1:]):
            # restrict the search to {Table} subclasses
            if isinstance(base, cls):
                # add the columns from this ancestor to the pile
                inherited.extend(base.pyre_localColumns)

        # build the tuple of all my columns
        table.pyre_columns = tuple(inherited + local)

        # and return the table record
        return table


    def __init__(self, name, bases, attributes, **kwds):
        # chain to the ancestors
        super().__init__(name, bases, attributes, **kwds)
        # all done
        return


    def __call__(self, **kwds):
        """
        Disable the instantiation of tables
        """
        import journal
        firewall = journal.firewall("pyre.db")
        raise firewall.log("database tables cannot be instantiated", stackdepth=-1)


# end of file 
