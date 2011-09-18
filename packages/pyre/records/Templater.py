# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# i am an attribute classifier
from ..patterns.AttributeClassifier import AttributeClassifier


# declaration
class Templater(AttributeClassifier):
    """
    Metaclass that inspects record declarations and endows their instances with the necessary
    infrastructure to support

    * named access of the entries in a record
    * composition via inheritance
    * derivations, i.e. fields whose values depend on the values of other fields
    """


    # types
    from .Entry import Entry as entry
    from .Field import Field as field
    from .Derivation import Derivation as derivation


    # meta methods
    def __new__(cls, name, bases, attributes, *, slots=None, **kwds):
        """
        Scan through the class attributes and harvest the record entries; adjust the attribute
        dictionary; build the class record for a new {Record} class
        """
        # initialize the local entry pile
        localEntries = []
        # harvest the entries
        for entryName, entry in cls.pyre_harvest(attributes, cls.entry):
            # adjust the name
            entry.name = entryName
            # update the aliases
            entry.aliases.add(entryName)
            # and add it to the pile
            localEntries.append(entry)

        # create and attribute to hold the locally declared records entries
        attributes["pyre_localEntries"] = tuple(localEntries)

        # remove the harvested attributes from the class dictionary; we will replace them with
        # record accessors in __init__. this can't be done while harvesting since it modifies
        # the attribute dictionary we are iterating over
        for entry in localEntries: del attributes[entry.name]

        # disable the wasteful __dict__
        if slots is not None: attributes["__slots__"] = slots

        # build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)

        # now that the class record is built, we can hunt down inherited entries
        # prime the inherited pile
        inheritedEntries = []
        # traverse the mro in _reverse_ order
        # for consistency, we place inherited entries ahead of local ones; derivations are
        # expressions involving any of the entries accessible at the point of their
        # declaration, so all of them must have been populated already
        for base in reversed(record.__mro__[1:]):
            # narrow down to my instances
            if isinstance(base, cls):
                # add entries form this ancestor
                inheritedEntries.extend(base.pyre_localEntries)

        # build the tuple of all my entries
        record.pyre_entries = tuple(inheritedEntries + localEntries)
        # build the tuple of all my fields
        record.pyre_fields = tuple(
            entry for entry in record.pyre_entries if isinstance(entry, cls.field))
        # build the tuple of all my derivations
        record.pyre_derivations = tuple(
            entry for entry in record.pyre_entries if isinstance(entry, cls.derivation))

        # all done
        return record


    def __init__(self, name, bases, attributes, **kwds):
        """
        Construct the index that maps descriptors to entry offsets
        """
        # first, get my superclass to do its thing
        super().__init__(name, bases, attributes, **kwds)
        # initialize the entry index
        subscripts = {}
        # enumerate my entries
        for index, entry in enumerate(self.pyre_entries):
            # record the index of this entry
            subscripts[entry] = index
        # attach the subscript index
        self.pyre_index = subscripts
        # and return
        return


# end of file 
