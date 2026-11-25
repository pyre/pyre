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
    from .FieldReference import FieldReference as pyre_reference
    from .Index import Index as pyre_index

    # meta methods
    def __new__(cls, name, bases, attributes, id=None, **kwds):
        # chain up
        table = super().__new__(cls, name, bases, attributes, id=id, **kwds)

        # tables with public names
        if id is not None:
            # get added to the global schema
            table.pyre_schema.tables.add(table)

        # now that the class record is built, collect what my bases declared: the fields of
        # the primary key
        primary = []
        # the groups of fields whose values are unique
        unique = []
        # the foreign keys
        foreign = []
        # the checks
        constraints = []
        # and the indexes
        indexes = []
        # go through my ancestors, the most distant first
        for base in reversed(table.__mro__[1:]):
            # restrict the search to tables
            if not isinstance(base, cls):
                # by moving on
                continue
            # each one carries what its own bases declared, so merge, leaving out what is there
            # already: the fields of the primary key
            cls._pyre_merge(target=primary, entries=base._pyre_primaryKeys)
            # the unique groups
            cls._pyre_merge(target=unique, entries=base._pyre_uniqueKeys)
            # the foreign keys
            cls._pyre_merge(target=foreign, entries=base._pyre_foreignKeys)
            # the checks
            cls._pyre_merge(target=constraints, entries=base._pyre_constraints)
            # and the indexes
            cls._pyre_merge(target=indexes, entries=base._pyre_indexes)

        # what my bases declared about the fields i shadow applies to the fields that replace
        # them; the checks, and the predicates of the indexes, name their fields by name, so they
        # apply as they are
        shadows = table.pyre_shadows
        # if i shadow any fields
        if shadows:
            # move the fields of the primary key
            primary = [shadows.get(field, field) for field in primary]
            # those of the unique groups
            unique = [
                (tuple(shadows.get(field, field) for field in fields), name)
                for fields, name in unique
            ]
            # the fields that refer to other tables
            foreign = [
                (
                    (
                        cls.pyre_reference(table=table, field=shadows[local.field])
                        if local.field in shadows
                        else local
                    ),
                    reference,
                    name,
                )
                for local, reference, name in foreign
            ]
            # and the fields of the indexes
            indexes = [
                cls.pyre_index(
                    fields=tuple(shadows.get(field, field) for field in index.fields),
                    unique=index.unique,
                    where=index.where,
                    name=index.name,
                )
                for index in indexes
            ]

        # save my primary keys
        table._pyre_primaryKeys = primary
        # save my unique fields
        table._pyre_uniqueKeys = unique
        # save my foreign key specs
        table._pyre_foreignKeys = foreign
        # save my constraints
        table._pyre_constraints = constraints
        # and my indexes
        table._pyre_indexes = indexes

        # and return the table record
        return table

    @staticmethod
    def _pyre_merge(target, entries):
        """
        Add to {target} the {entries} it does not hold already, in their order
        """
        # go through the entries
        for entry in entries:
            # the ones {target} holds already, which are the same objects
            if any(existing is entry for existing in target):
                # are left alone
                continue
            # the others are added at the end
            target.append(entry)
        # all done
        return target

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
