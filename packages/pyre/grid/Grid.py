# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# support
from .Tile import Tile


# declaration
class Grid:
    """
    A logically cartesian grid
    """


    # meta-methods
    def __init__(self, shape, layout=None, value=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # make a tile out of my shape and layout
        self.tile = Tile(shape=shape, layout=layout)

        # compute the tile size
        size = self.tile.size

        # if {value} is callable
        if callable(value):
            # build my data by invoking it once per cell
            self.data = [ value() for _ in range(size) ]
        # otherwise
        else:
            # make a list filled with value
            self.data = [ value ] * size

        # all done
        return


    def __getitem__(self, index):
        """
        Return the value stored at {index}
        """
        # tile knows the offset
        return self.data[self.tile.offset(index)]


    def __setitem__(self, index, value):
        """
        Return the value stored at {index}
        """
        # tile knows the offset
        self.data[self.tile.offset(index)] = value
        # all done
        return


# end of file
