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


# end of file 
