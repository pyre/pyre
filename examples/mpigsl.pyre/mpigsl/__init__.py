# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# the test harness
from .Partitioner import Partitioner as partitioner


# convenience functions
def scatter(shape, matrix=None, source=0, communicator=None):
    """
    Scatter {matrix} held by the {source} tasks among all tasks in {communicator}. Only
    {source} has to provide a {matrix}; the other tasks can use the default. Each task gets a
    matrix whose layout is described by {shape}.
    """
    # normalize the communicator
    if communicator is None:
        # get the mpi package
        import mpi
        # use the world by default
        communicator = mpi.world
    # get its capsule
    mpicomm = communicator.capsule

    # get the matrix capsule
    data = None if matrix is None else matrix.data

    # get the extension
    from . import mpigsl
    # make the call
    partition = mpigsl.scatter(mpicomm, source, data, shape)

    # get the gsl package
    import gsl
    # dress up my local portion as a matrix
    result = gsl.matrix(shape=shape, data=partition)
    # and return it
    return result
        

def gather(matrix, destination=0, communicator=None):
    """
    Gather the {matrix} contributions from all tasks in {communicator} into a new matrix
    available only at the {destination} task
    """
    # normalize the communicator
    if communicator is None:
        # get the mpi package
        import mpi
        # use the world by default
        communicator = mpi.world


# end of file 
