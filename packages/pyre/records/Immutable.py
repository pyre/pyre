# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# superclass
from .Templater import Templater


# declaration
class Immutable(Templater):
    """
    Metaclass for records whose entries are immutable
    """


    # types
    from .ConstAccessor import ConstAccessor as pyre_accessor


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Scan through the class attributes and harvest the record entries; adjust the attribute
        dictionary; build the class record for a new immutable {Record} class
        """
        # build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)

        # inspect the record and install an appropriate data processor
        # if there are no derivations present in this record
        if not record.pyre_derivations:
            # use fast processing
            record.pyre_processEntries = record.pyre_processFields
        # otherwise
        else:
            # use the slower method that enables inter-column data access
            record.pyre_processEntries = record.pyre_processFieldsAndDerivations

        # all done
        return record


    def __init__(self, name, bases, attributes, **kwds):
        """
        Decorate a new minted {Record} subclass

        Now that the class record is built, we iterate over all entries and build the accessors
        that will convert named access through the descriptors into indexed access to the
        underlying tuple
        """
        # first, get my superclass to do its thing
        super().__init__(name, bases, attributes, **kwds)

        # initialize the entry index
        subscripts = {}
        # enumerate my entries
        for index, entry in enumerate(self.pyre_entries):
            # record the index of this entry
            subscripts[entry] = index
            # create the data accessor 
            accessor = self.pyre_accessor(entry=entry, index=index)
            # and attach it
            setattr(self, entry.name, accessor)
        # attach the subscript index
        self.pyre_index = subscripts
        # and return
        return


# end of file 
