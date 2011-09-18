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
        # build the class record; disable the wasteful __dict__
        record = super().__new__(cls, name, bases, attributes, slots=(), **kwds)

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
        Decorate a newly minted immutable record subclass

        Now that the class record is built, we iterate over all entries and build the accessors
        that will convert named access through the descriptors into indexed access to the
        underlying tuple
        """
        # first, get my superclass to do its thing
        super().__init__(name, bases, attributes, **kwds)

        # enumerate my entries
        for index, entry in enumerate(self.pyre_entries):
            # create the data accessor 
            accessor = self.pyre_accessor(entry=entry, index=index)
            # and attach it
            setattr(self, entry.name, accessor)
        # all done
        return


# end of file 
