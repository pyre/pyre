# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# value storage
from .Field import Field as field


# utilities
def transfer(grid, fields, mesh):
    """
    Transfer the {fields} defined over a grid to fields defined over the {mesh}
    """
    # initialize the result
    xfer = { property: [] for property in fields.keys() }

    # get the dimension of the grid
    dim = len(grid.shape)
    # and its shape
    ni, nj, nk = grid.shape

    # here we go: for every tet
    for tetid, tet in enumerate(mesh.simplices):
        # get the coordinates of its nodes
        vertices = tuple(mesh.points[node] for node in tet)
        # compute the barycenter
        bary = tuple(sum(point[i] for point in vertices)/4 for i in range(3))

        # initialize the search bounds
        imin = [0] * dim
        imax = list(n-1 for n in grid.shape)

        # as long as the two end points haven't collapsed
        while imin < imax:
            # find the midpoint
            index = [(high+low)//2 for low, high in zip(imin, imax)]
            # get that cell
            cell = grid[index]
            # get one corner of its bounding box
            cmin = tuple(min(p[i] for p in cell) for i in range(dim))
            # get the other corner of its bounding box
            cmax = tuple(max(p[i] for p in cell) for i in range(dim))
            # decide which way to go
            for d in range(dim):
                # if {bary} is smaller than that
                if bary[d] < cmin[d]:
                    imax[d] = max(imin[d], index[d] - 1)
                # if {bary} is greater than that
                elif bary[d] > cmax[d]:
                    imin[d] = min(imax[d], index[d] + 1)
                # if {bary} is within
                elif cmin[d] <= bary[d] <= cmax[d]:
                    imin[d] = index[d]
                    imax[d] = index[d]
                else:
                    assert False, 'could not locate grid cell for tet {}'.format(tetid)

        # ok. we found the index; transfer the fields
        for property, field in fields.items():
            # store the value
            xfer[property].append(field[imin])

    # all done; return the map of transferred fields
    return xfer


# end of file 
