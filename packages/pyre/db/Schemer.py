# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# the base class that triggers descriptor sniffing
from ..patterns.AttributeClassifier import AttributeClassifier


# declaration
class Schemer(AttributeClassifier):
    """
    Metaclass that inspects a table declaration and builds the information necessary to connect
    its attributes to the fields of the underlying table in the database back end
    """


    # types
    from .Field import Field


    # meta methods
    def __new__(cls, name, bases, attributes, id=None, alias=None, **kwds):
        # chain to my ancestor
        table = super().__new__(cls, name, bases, attributes, **kwds)

        # set up the table name
        table.pyre_name = name if id is None else id
        table.pyre_alias = table.pyre_name if alias is None else alias
        # harvest the locally declared fields
        local = []
        for fieldName, field in cls.pyre_harvest(attributes, cls.Field):
            # set the name of the field
            field.name = fieldName
            # add it to the pile
            local.append(field)
        # store the harvested fields
        table.pyre_localFields = tuple(local)

        # now that the class record is built, we can hunt down inherited attributes
        inherited = []
        primary = set()
        unique = set()
        foreign = []
        constraints = []
        knownFields = set()
        # traverse the mro
        for base in table.__mro__:
            # restrict the search to {Table} subclasses
            if not isinstance(base, cls): continue
            # iterate over the fields declared locally in this ancestor
            for field in base.pyre_localFields:
                # if this field is shadowed by another with the same name, skip it
                if field in knownFields: continue
                # it's not shadowed; add it to the pile
                inherited.append(field)
                knownFields.add(field)
                # if this field is a primary key for its table
                if field in base._pyre_primaryKeys:
                    # then it is a primary key for mine too
                    primary.add(field)
                # if this field is unique over its table
                if field in base._pyre_uniqueFields:
                    # then it is unique for mine too
                    unique.add(field)
                # NYI: foreign keys
                # NYI: constraints

        # build the tuple of all my fields
        table.pyre_fields = tuple(inherited)
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


# end of file 
