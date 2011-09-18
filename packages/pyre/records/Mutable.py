# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# superclass
from .Templater import Templater


# declaration
class Mutable(Templater):
    """
    Metaclass for records whose entries are mutable.

    Mutable records are implemented using tuples of {pyre.calc} nodes. As a result, the values
    of fields may be modified after the original data ingestion, and all derivations are
    updated dynamically.
    """


    # types
    from .Accessor import Accessor as pyre_accessor


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Scan through the class attributes and harvest the record entries; adjust the attribute
        dictionary; build the class record for a new {Record} class
        """
        # disable the wasteful __dict__
        return super().__new__(cls, name, bases, attributes, slots=(), **kwds)


# end of file 
