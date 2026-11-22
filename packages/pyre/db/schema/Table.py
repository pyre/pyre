# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# metaclass
from .Schemer import Schemer

# superclass
from ... import records


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
    def pyre_unique(cls, *references):
        """
        Require that the fields of {references} be unique together across my rows; each call
        makes a constraint of its own
        """
        # record the fields, as one constraint
        cls._pyre_uniqueKeys.append(tuple(reference.field for reference in references))
        # and return
        return cls

    @classmethod
    def pyre_foreignKey(cls, field, foreign):
        """
        Mark {field} as a reference to {foreign}
        """
        # add an entry to the foreign key list
        cls._pyre_foreignKeys.append((field, foreign))
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

    # implementation details
    # table attributes that generate the table wide declaration statements; initialized by my
    # metaclass at compile time
    _pyre_primaryKeys = None  # the fields of my primary key, in order
    _pyre_uniqueKeys = None  # the groups of fields whose values are unique across my rows
    _pyre_foreignKeys = None  # my references to other tables
    _pyre_constraints = None  # and the checks my rows must pass


# end of file
