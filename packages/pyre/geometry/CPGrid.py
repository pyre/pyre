# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# my base class
from .Grid import Grid


# class declaration
class CPGrid(Grid):
    """
    A corner point grid is a collection of hexahedral cells each of which is defined by the
    corners of two of its faces
    """


    # interface
    def cell(self, corners):
        """
        Create a cell out of the coordinates of its eight corners
        """
        # make one
        cell = tuple(map(tuple, corners))
        # add it to my pile
        self.append(cell)
        # and return it
        return cell


    def boundingBox(self):
        """
        Compute the bounding box of the grid
        """
        # check the cache
        if self._bbox is not None:
            # return it
            return self._bbox
        # otherwise, compute the smallest value of the coordinate along each axis
        small = tuple(
            min(p[i] for cell in self for p in cell) for i in range(len(self.shape))
            )
        # and the largest value of the coordinate along each axis
        large = tuple(
            max(p[i] for cell in self for p in cell) for i in range(len(self.shape))
            )
        # cache it
        self._bbox = small, large
        # and return it
        return self._bbox


    def eigenlen(self):
        """
        Compute the characteristic scale of the mesh
        """
        # reset the bad cell list
        self.bad = []
        # compute the largest possible value for my characteristic scale
        inf = min(t-b for b,t in zip(*self.boundingBox()))
        # go through my cells and return the minimum change along any axis
        return min(
            self.scale(idx=idx, cell=cell, dim=len(self.shape)-1, inf=inf)
            for idx, cell in enumerate(self))


    # meta-methods
    def __init__(self, *args, **kwds):
        # chain up
        super().__init__(*args, **kwds)
        # initialize my bounding box
        self._bbox = None
        # bad cell info
        self.bad = []
        # all done
        return


    # implementation details
    def scale(self, idx, cell, dim, inf):
        """
        Compute the smallest edge in {cell}
        """
        # compute half the number of points in the cell
        l = len(cell)//2
        # split the cell in two
        top = cell[:l]
        bottom = cell[l:]

        # compute the minimum of change along the {dim} axis
        h = min(abs(t[dim] - b[dim]) for t,b in zip(top, bottom))

        # guard against slivers
        if h == 0:
            # save the info
            self.bad.append((idx, dim, cell))
            # reset h
            h = inf

        # if we have reached the end
        if dim == 0:
            # return my minimum
            return h

        # otherwise return the minimum of my scale and whatever happens in the other dimensions
        return min(h, self.scale(idx, top, dim-1, inf), self.scale(idx, bottom, dim-1, inf))


    # debugging
    def verify(self):
        """
        Run some consistency checks
        """
        # compute the size implied by my shape
        size = 1
        for axis in self.shape: size *= axis
        # check the length
        assert len(self) == size, "wrong size: length: {}, computed size: {}".format(
            len(self), size)

        # my dimension
        dim = len(self.shape)
        # the number of points it takes to specify a cell
        spec = 2**dim

        # go through my contents
        for i, cell in enumerate(self):
            # the number of points in this cell
            l = len(cell)
            # and check they are dimensioned properly
            assert l == spec, "cell {}: wrong number of corners: {}, not {}".format(i, l, spec)
            # and that they contain
            for p, point in enumerate(cell):
                # the space dimension of this point
                d = len(point)
                # points of the correct dimension
                assert d == dim, "cell {}, point {}: wrong dimension: {}, not {}".format(
                    i, p, d, dim)

        # all done
        return


# end of file
