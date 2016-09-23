# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# index objects
def tile(**kwds):
    """
    Create a tile
    """
    # get the factory
    from .Tile import Tile
    # instantiate and return it
    return Tile(**kwds)


# end of file
