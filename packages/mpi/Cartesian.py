# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclasses
from .Communicator import Communicator


# declaration
class Cartesian(Communicator):
    """
    An encapsulation of Cartesian communicators
    """


    # per-instance public data
    axes = None
    periods = None
    coordinates = None


    # meta methods
    def __init__(self, handle, axes, periods, reorder, **kwds):
        # build the handle of the Cartesian communicator
        cartesian = self.mpi.communicatorCreateCartesian(handle, reorder, axes, periods)

        # chain to my ancestors
        super().__init__(handle=cartesian, **kwds)

        # save the rest
        self.axes = axes
        self.periods = periods
        # get my coördinates
        self.coordinates = self.mpi.communicatorCartesianCoordinates(
            self._handle, self.rank, len(axes))

        # all done
        return


# end of file 
