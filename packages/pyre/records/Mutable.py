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
    def __init__(self, name, bases, attributes, **kwds):
        """
        Decorate a newly minted mutable record subclass

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
