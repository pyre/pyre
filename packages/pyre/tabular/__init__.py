# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


# access to the basic object in the package
from .Sheet import Sheet as sheet


# descriptors
def auto(**kwds):
    """
    Build a descriptor that corresponds to a field that is automatically retrieved from the
    data store by looking up an entry by the same name
    """
    # access measure
    from .Measure import Measure
    # build one and return it
    return Measure(**kwds)


# end of file 
