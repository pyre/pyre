# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# metaclass
from .Schemer import Schemer

# superclass
from ... import records

# the indexes over my fields
from .Index import Index


# declaration
class Table(records.record, metaclass=Schemer):
    """
    Base class for database table declarations
    """

    # constants
    from .literals import default, null
    from ..queries.expressions import IsNull as isNull, IsNotNull as isNotNull

    # interface
    # declaration decorators
    @classmethod
    def pyre_primaryKey(cls, reference):
        """
        Add the field of {reference} to my primary key, after the ones added before it
        """
        # get the field
        field = reference.field
        # a field already in the key
        if any(key is field for key in cls._pyre_primaryKeys):
            # stays where it is
            return cls
        # the others are added at the end
        cls._pyre_primaryKeys.append(field)
        # and return
        return cls

    @classmethod
    def pyre_unique(cls, *references, name=None):
        """
        Require that the fields of {references} be unique together across my rows; each call
        makes a constraint of its own, which goes by {name} when it is given one
        """
        # record the fields, as one constraint, along with its name
        cls._pyre_uniqueKeys.append((tuple(reference.field for reference in references), name))
        # and return
        return cls

    @classmethod
    def pyre_index(cls, *references, unique=False, where=None, name=None):
        """
        Index my rows by the fields of {references}, in order; {unique} forbids two rows to share
        their values, {where} restricts the index to the rows that pass it, and {name} replaces
        the one made of my name and those of the fields; each call makes an index of its own
        """
        # record the index
        cls._pyre_indexes.append(
            Index(
                fields=tuple(reference.field for reference in references),
                unique=unique,
                where=where,
                name=name,
            )
        )
        # and return
        return cls

    @classmethod
    def pyre_foreignKey(cls, field, foreign, name=None):
        """
        Mark {field} as a reference to {foreign}; the constraint goes by {name} when it is given
        one
        """
        # add an entry to the foreign key list, along with its name
        cls._pyre_foreignKeys.append((field, foreign, name))
        # and return
        return cls

    @classmethod
    def pyre_check(cls, expression, name=None):
        """
        Require my rows to pass {expression}; the constraint goes by {name} when it is given one
        """
        # add {expression} to my pile of constraints, along with its name
        cls._pyre_constraints.append((expression, name))
        # and return
        return cls

    # implementation details
    # table attributes that generate the table wide declaration statements; initialized by my
    # metaclass at compile time
    _pyre_primaryKeys = None  # the fields of my primary key, in order
    _pyre_uniqueKeys = None  # the groups of fields whose values are unique across my rows, named
    _pyre_foreignKeys = None  # my references to other tables, named
    _pyre_constraints = None  # the checks my rows must pass, named
    _pyre_indexes = None  # and the indexes over my fields


# end of file
