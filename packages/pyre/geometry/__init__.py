# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# triangulated surfaces
def surface(**kwds):
    """
    Create a surface
    """
    # get the factory
    from .Surface import Surface

    # make one and return it
    return Surface(**kwds)


# logically cartesian grids
def grid(**kwds):
    """
    Create a grid
    """
    # get the factory
    from .Grid import Grid

    # make on and return it
    return Grid(**kwds)


# corner-point grids
def cpg(**kwds):
    """
    Create a corner point grid
    """
    # get the factory
    from .CPGrid import CPGrid

    # make one and return it
    return CPGrid(**kwds)


# simple representation of a simplicial mesh
def mesh(**kwds):
    """
    Create a mesh
    """
    # get the factory
    from .Mesh import Mesh

    # make one and return it
    return Mesh(**kwds)


# value storage
def field(**kwds):
    """
    Create a field over a one of the space discretizations
    """
    # get the factory
    from .Field import Field

    # make one and return it
    return Field(**kwds)


# converters
def triangulation(**kwds):
    """
    Create a triangulation
    """
    # get the factory
    from .Triangulation import Triangulation

    # make one and return it
    return Triangulation(**kwds)


# spaces
def timeline(epoch=None):
    """
    Create the line of time with the given {epoch}, by default the start of 1970 in UTC
    """
    # get the factory
    from .Timeline import Timeline

    # make one and return it
    return Timeline(epoch=epoch)


# constructions
def union(*shapes):
    """
    The union of the given {shapes}
    """
    # get the bindings
    from .. import libpyre

    # and ask them
    return libpyre.geometry.union(shapes=list(shapes))


def hull(a, b):
    """
    The smallest shape that holds both {a} and {b}
    """
    # get the bindings
    from .. import libpyre

    # and ask them
    return libpyre.geometry.hull(a=a, b=b)


# relations
def intersects(a, b):
    """
    Check whether {a} and {b} share a point
    """
    # get the bindings
    from .. import libpyre

    # and ask them
    return libpyre.geometry.intersects(a=a, b=b)


def covers(a, b):
    """
    Check whether every point of {b} is a point of {a}
    """
    # get the bindings
    from .. import libpyre

    # and ask them
    return libpyre.geometry.covers(a=a, b=b)


# utilities
def transfer(grid, fields, mesh):
    """
    Transfer the {fields} defined over a grid to fields defined over the {mesh}
    """
    # initialize the result
    xfer = {property: [] for property in fields.keys()}

    # get the dimension of the grid
    dim = len(grid.shape)

    # here we go: for every tet
    for tetid, tet in enumerate(mesh.simplices):
        # get the coordinates of its nodes
        vertices = tuple(mesh.points[node] for node in tet)
        # compute the barycenter
        bary = tuple(sum(point[i] for point in vertices) / len(vertices) for i in range(dim))

        # initialize the search bounds: from the first cell
        imin = [0] * dim
        # to the last one
        imax = list(n - 1 for n in grid.shape)

        # as long as the two end points haven't collapsed
        while imin < imax:
            # find the midpoint
            index = [(high + low) // 2 for low, high in zip(imin, imax)]
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
                    # look below the midpoint
                    imax[d] = max(imin[d], index[d] - 1)
                # if {bary} is greater than that
                elif bary[d] > cmax[d]:
                    # look above it
                    imin[d] = min(imax[d], index[d] + 1)
                # if {bary} is within
                elif cmin[d] <= bary[d] <= cmax[d]:
                    # the cell is found, so collapse the lower bound onto it
                    imin[d] = index[d]
                    # and the upper one
                    imax[d] = index[d]
                # a barycenter that compares with nothing
                else:
                    # can't be placed in any cell
                    assert False, f"could not locate grid cell for tet {tetid}"

        # ok. we found the index; transfer the fields
        for property, field in fields.items():
            # store the value
            xfer[property].append(field[imin])

    # all done; return the map of transferred fields
    return xfer


def boxUnion(b1, b2):
    """
    Compute a box big enough to contain both input boxes
    """
    # easy enough
    return tuple(map(min, zip(b1[0], b2[0]))), tuple(map(max, zip(b1[1], b2[1])))


def boxIntersection(b1, b2):
    """
    Compute a box small enough  to fit inside both input boxes
    """
    # easy enough
    return tuple(map(max, zip(b1[0], b2[0]))), tuple(map(min, zip(b1[1], b2[1])))


def convexHull(points):
    """
    Compute the convex hull of the given {points}
    """
    # set up the two corners: the lowest one
    p_min = []
    # and the highest one
    p_max = []
    # zip all the points together, forming as many streams of coordinates as there are
    # dimensions
    for axis in zip(*points):
        # store the minimum value in p_min
        p_min.append(min(axis))
        # and the maximum value in p_max
        p_max.append(max(axis))
    # all done
    return p_min, p_max


# end of file
