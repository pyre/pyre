# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..patterns.AttributeClassifier import AttributeClassifier


class Templater(AttributeClassifier):
    """
    Metaclass that inspects records and extracts their item descriptors

    {Templater} is responsible for adjusting {Record} declarations in order to preserve the
    information necessary to support

    * named access of record items
    * composition via inheritance
    * derivations, i.e. items whose values are computed using the values of other items
    """


    # types
    from .Field import Field
    from .FieldProxy import FieldProxy
    from .Derivation import Derivation
    from ..algebraic.Node import Node
    from ..algebraic.Operator import Operator


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Scan through the class attributes and harvest the locally declared items, adjust the
        attribute dictionary, and build the class record for a new {Record} class
        """
        # harvest the items
        localItems = []
        for itemName, item in cls.pyre_harvest(attributes, cls.Node):
            # check whether this is an {Operator} instance
            if isinstance(item, cls.Operator):
                # convert it into a derivation
                item = cls.Derivation(name=itemName, expression=item)
            # otherwise
            else:
                # record its name
                item.name = itemName
                # if this is a regular {Field}
                if isinstance(item, cls.Field):
                    # place its name in the set of its aliases
                    item.aliases.add(itemName)
            # and add it to the pile
            localItems.append(item)

        # create an attribute to hold the locally declared items
        attributes["pyre_localItems"] = tuple(localItems)
                
        # remove the harvested attributes from the class dictionary, for now
        # we will replace them with record specific accessors in __init__
        for item in localItems: del attributes[item.name]

        # disable the wasteful __dict__
        attributes["__slots__"] = ()
        
        # build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)

        # now that the class record is built, we can hunt down inherited items
        inheritedItems = []
        # traverse the mro
        for base in reversed(record.__mro__[1:]):
            # narrow the search down to my instances, i.e. {Record} subclasses
            if isinstance(base, cls):
                # add this ancestor's items
                inheritedItems.extend(base.pyre_localItems)

        # build the tuple of all my items
        record.pyre_items = tuple(inheritedItems + localItems)
        # build the tuple of my fields
        record.pyre_fields = tuple(
            item for item in record.pyre_items if isinstance(item, cls.Field))
        # build the tuple of my derivations
        record.pyre_derivations = tuple(
            item for item in record.pyre_items if isinstance(item, cls.Derivation))

        # if the record has no derivations
        if record.pyre_derivations == ():
            # use fast processing
            record.pyre_process = record.pyre_processFields
        # otherwise
        else:
            # use the slower one that enables inter-column data access
            record.pyre_process = record.pyre_processFieldsAndDerivations
            # quick access to the record fields
            fields = set(record.pyre_fields)
            # the field proxies: the field replacements in the derivation expressions
            proxies = {}
            # loop over the derivations
            for derivation in record.pyre_derivations:
                # and for every node in the dependency list
                for item in derivation.dependencies:
                    # check whether it an actual field
                    if item not in fields: continue
                    # if we have not built a proxy for this one yet, do so
                    if item not in proxies: proxies[item] = cls.FieldProxy(field=item)
                # patch this derivation
                derivation.substitute(proxies)
            # and store the proxies with the record
            # N.B.: only used for debugging for the time being
            record.pyre_proxies = proxies

        # return the record
        return record


    def __init__(self, name, bases, attributes, **kwds):
        """
        Decorate a newly minted {Record} class

        Now that the class record is built, we can hunt down inherited items and build the
        accessors that will convert named access through the descriptors into indexed access
        into the underlying tuple
        """
        # first, get my superclass to do its thing
        super().__init__(name, bases, attributes, **kwds)

        # initialize the item index
        subscripts = {}
        # enumerate my items
        for index, item in enumerate(self.pyre_items):
            # record the index of this item
            subscripts[item] = index
            # build the data accessor
            accessor = item.pyre_recordFieldAccessor(record=self, index=index)
            # and attach it
            setattr(self, item.name, accessor)
        # attach the subscript index
        self.pyre_index = subscripts

        # and return
        return


# end of file 
