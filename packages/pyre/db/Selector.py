# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access to {OrderedDict}
import collections
# the base class that triggers descriptor sniffing
from ..patterns.AttributeClassifier import AttributeClassifier


# declaration
class Selector(AttributeClassifier):
    """
    Metaclass that inspects a query declaration and collects the information necessary to build
    the corresponding SELECT expressions
    """


    # types
    # local
    from .Entry import Entry as pyre_Entry
    from .Schemer import Schemer as pyre_Schemer
    from .FieldReference import FieldReference as pyre_FieldReference
    # borrowed
    from ..records import record as pyre_Record
    from ..records import field as pyre_RecordDescriptor


    # data
    pyre_reserved = {"where", "group", "order"}


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
                # derive a new class from it so we can change the table name to the local alias
                alias = cls.pyre_Schemer(name, (value,), {}, alias=value.pyre_name)
                # add it to the pile
                aliases.add(alias)
                # and make it accessible as an attribute
                attributes[name] = alias

        # now, go through each of the bases to make tables from ancestor queries available in
        # the local scope of the class declaration so users don't have to stand on their head
        # to get access to them
        for base in bases:
            # skip bases that are not queries
            if not isinstance(base, cls): continue
            # queries contribute their aliased tables to my attributes
            attributes.update((table.pyre_name, table) for table in base.pyre_tables)

        # prime the table aliases
        attributes["pyre_tables"] = aliases
                
        # return the attribute container
        return attributes

        
    def __new__(cls, name, bases, attributes, hidden=False, **kwds):
        # chain to my ancestor
        query = super().__new__(cls, name, bases, attributes, **kwds)
        # leave early if this is a pyre internal class
        if hidden: return query

        # prime the pile of fields
        fields = []
        # the set of referenced tables
        tables = set()
        # and the field descriptors
        descriptors = collections.OrderedDict()

        # iterate over the important attributes
        for name, entry in cls.pyre_harvest(attributes, cls.pyre_Entry):
            # skip the special attributes
            if name in cls.pyre_reserved: continue
            # decorate the entry with its name
            entry.name = name
            # add it to the pile
            fields.append(entry)
            # if the entry is a field reference
            if isinstance(entry, cls.pyre_FieldReference):
                # add the referenced table to the pile
                tables.add(entry.table)

            # figure out the type of the entry so we can cast it properly
            types = { variable.schema for variable in entry.variables }
            # if there is only one type
            if len(types) == 1:
                # get it
                converter = types.pop()
            # otherwise
            else:
                # type promotions
                raise NotImplementedError("NYI: Selector.__new__: type promotions")

            # make a record field descriptor
            descriptor = cls.pyre_RecordDescriptor()
            # attach its type
            descriptor.schema = converter
            # and add it to the pile
            descriptors[name] = descriptor

        # record the field references
        query.pyre_localFields = tuple(fields)
        # and the associated descriptors
        query.pyre_localDescriptors = descriptors

        # interpret inheritance as composition; the only trickiness arises when subclasses
        # shadow names from their base classes. the treatment here is consistent with
        # {pyre.records.Templater}, which creates record slots in the order that they are
        # encountered in the mro, regardless of whether the names are shadowed

        # initialize the set of fields
        fields = []
        # and the field descriptors
        descriptors = collections.OrderedDict()
        # iterate over the base classes
        for base in reversed(query.__mro__):
            # narrow down to my instances
            if not isinstance(base, cls): continue
            # collect entries from this ancestor
            fields += list(base.pyre_localFields)
            tables |= base.pyre_tables
            descriptors.update(base.pyre_localDescriptors)

        # record the field references
        query.pyre_fields = tuple(fields)
        # add the tables references to the query pile
        query.pyre_tables |= tables
        # build the record type
        query.pyre_Record = type(name + "_pyreRecord", (cls.pyre_Record,), descriptors)

        # return the query class record
        return query


# end of file 
