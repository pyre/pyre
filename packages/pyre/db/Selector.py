# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# the base class that triggers descriptor sniffing
from ..patterns.AttributeClassifier import AttributeClassifier


# declaration
class Selector(AttributeClassifier):
    """
    Metaclass that inspects a query declaration and collects the information necessary to build
    the corresponding SELECT expressions
    """


    # types
    from .Schemer import Schemer as pyre_Schemer
    from .FieldReference import FieldReference as pyre_FieldReference
    pyre_Derivation = pyre_FieldReference.operator


    # meta methods
    @classmethod
    def __prepare__(cls, name, bases, hidden=False, **kwds):
        """
        Build an attribute table that contains the local table aliases
        """
        # delegate to my superclasses
        attributes = super().__prepare__(name, bases)
        # leave early if this is an internal class
        if hidden: return attributes

        # the table aliases
        aliases = set()

        # look through {kwds} for table aliases
        for name, value in kwds.items():
            # if {value} is a table
            if isinstance(value, cls.pyre_Schemer):
                # derive a class from it
                alias = cls.pyre_Schemer(name, (value,), {}, alias=value.pyre_name)
                # add it to the pile
                aliases.add(alias)
                # and make it accessible as an attribute
                attributes[name] = alias

        # prime the table aliases
        attributes["pyre_tables"] = aliases
                
        # return the attribute container
        return attributes

        
    def __new__(cls, name, bases, attributes, hidden=False, **kwds):
        # chain to my ancestor
        query = super().__new__(cls, name, bases, attributes, **kwds)
        # leave early if this is a pyre internal class
        if hidden: return query

        # extract the field references
        query.pyre_fields = tuple(cls.pyre_harvest(attributes, cls.pyre_FieldReference))
        query.pyre_derivations = tuple(cls.pyre_harvest(attributes, cls.pyre_Derivation))

        # add the tables references to the query pile
        query.pyre_tables |= set(ref.table for name, ref in query.pyre_fields)

        # return the query class record
        return query


# end of file 
