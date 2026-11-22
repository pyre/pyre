# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from ... import records

# the strategy that builds the rows read from a server
from .Verbatim import Verbatim


# declaration
class Schemer(records.templater):
    """
    Metaclass that inspects a table declaration and builds the information necessary to connect
    its attributes to the fields of the underlying table in the database back end
    """

    # types
    from .FieldSelector import FieldSelector as pyre_selector

    # meta methods
    def __new__(cls, name, bases, attributes, id=None, **kwds):
        # chain up
        table = super().__new__(cls, name, bases, attributes, id=id, **kwds)

        # tables with public names
        if id is not None:
            # get added to the global schema
            table.pyre_schema.tables.add(table)

        # now that the class record is built, we can hunt down inherited attributes: the
        # fields of the primary key
        primary = set()
        # the fields whose values are unique
        unique = set()
        # the foreign keys
        foreign = []
        # and the constraints
        constraints = []
        # traverse the mro
        for base in reversed(table.__mro__):
            # restrict the search to {Table} subclasses
            if not isinstance(base, cls):
                # by moving on
                continue
            # iterate over the fields declared locally in this ancestor
            for field in base.pyre_localFields:
                # if this field is a primary key for its table
                if field in base._pyre_primaryKeys:
                    # then it is a primary key for mine too
                    primary.add(field)
                # if it is unique over its table
                if field in base._pyre_uniqueFields:
                    # then it is unique for mine too
                    unique.add(field)
                # NYI: foreign keys
                # NYI: constraints

        # save my primary keys
        table._pyre_primaryKeys = primary
        # save my unique fields
        table._pyre_uniqueFields = unique
        # save my foreign key specs
        table._pyre_foreignKeys = foreign
        # save my constraints
        table._pyre_constraints = constraints

        # and return the table record
        return table

    def __init__(self, name, bases, attributes, **kwds):
        # chain up, which builds the generators of my rows
        super().__init__(name, bases, attributes, **kwds)
        # the rows read from a server take their values as they are, since the server turned
        # each one into its type
        self.pyre_storedTuple = type(
            "stored", (self.pyre_immutableTuple,), {"__slots__": (), "pyre_extract": Verbatim()}
        )
        # all done
        return


# end of file
