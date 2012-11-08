# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Partitioner:
    """
    A class to exercise partitioning a gsl matrix among mpi tasks
    """


    # interface
    def partition(self, taskload, communicator=None, source=0, matrix=None):
        """
        Scatter {matrix} held by the {source} tasks among all tasks in {communicator}. Only
        {source} has to provide a {matrix}; the other tasks can use the default. Each task gets
        a matrix whose layout is described by {taskload}.
        """
        # normalize the communicator
        if communicator is None:
            # get the mpi package
            import mpi
            # use the world by default
            communicator = mpi.world

        # get the matrix capsule
        data = None if matrix is None else matrix.data

        # get the extension
        from . import mpigsl
        # make the call
        partition = mpigsl.scatter(communicator.capsule, source, data, taskload)

        # get the gsl package
        import gsl
        # dress up my local portion as a matrix
        result = gsl.matrix(shape=taskload, data=partition)
        # and return it
        return result


    def collect(self, matrix, communicator=None, destination=0):
        """
        Gather the data in {matrix} from each task in {communicator} into one big matrix
        available at the {destination} task
        """
        # normalize the communicator
        if communicator is None:
            # get the mpi package
            import mpi
            # use the world by default
            communicator = mpi.world

        # get the extension
        from . import mpigsl
        # make the call
        result = mpigsl.gather(communicator.capsule, destination, matrix.data)

        # if i am not the destination task, nothing further to do
        if communicator.rank != destination: return

        # otherwise, get the gsl package
        import gsl
        # unpack the result
        data, shape = result
        # dress up the result as a matrix
        return gsl.matrix(shape=shape, data=data)


# end of file 
