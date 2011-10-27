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
    def __new__(cls, name, bases, attributes, id=None, alias=None, **kwds):
        # chain to my ancestor
        table = super().__new__(cls, name, bases, attributes, **kwds)

        # set up the table name
        table.pyre_name = name if id is None else id
        table.pyre_alias = table.pyre_name if alias is None else alias
        # harvest the locally declared columns
        local = []
        for columnName, column in cls.pyre_harvest(attributes, cls.Column):
            # set the name of the column
            column.name = columnName
            # add it to the pile
            local.append(column)
        # store the harvested columns
        table.pyre_localColumns = tuple(local)

        # now that the class record is built, we can hunt down inherited attributes
        inherited = []
        primary = set()
        unique = set()
        foreign = []
        constraints = []
        knownColumns = set()
        # traverse the mro
        for base in table.__mro__:
            # restrict the search to {Table} subclasses
            if not isinstance(base, cls): continue
            # iterate over the columns declared locally in this ancestor
            for column in base.pyre_localColumns:
                # if this column is shadowed by another with the same name, skip it
                if column in knownColumns: continue
                # it's not shadowed; add it to the pile
                inherited.append(column)
                knownColumns.add(column)
                # if this column is a primary key for its table
                if column in base._pyre_primaryKeys:
                    # then it is a primary key for mine too
                    primary.add(column)
                # if this column is unique over its table
                if column in base._pyre_uniqueColumns:
                    # then it is unique for mine too
                    unique.add(column)
                # NYI: foreign keys
                # NYI: constraints

        # build the tuple of all my columns
        table.pyre_columns = tuple(inherited)
        # save my primary keys
        table._pyre_primaryKeys = primary
        # save my unique columns
        table._pyre_uniqueColumns = unique
        # save my foreign key specs
        table._pyre_foreignKeys = foreign
        # save my constraints
        table._pyre_constraints = constraints

        # and return the table record
        return table


# end of file 
