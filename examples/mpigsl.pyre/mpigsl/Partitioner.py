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
    def partition(self, sampleSize, samplesPerTask):
        """
        Verify that we can build a gsl matrix whose shape is (samples per task x number of
        tasks) by sampleSize and scatter it among the mpi tasks
        """
        # access the external packages
        import mpi
        import gsl
        # access my extension
        from . import scatter, gather

        # figure out the machine layout
        world = mpi.world
        tasks = world.size
        rank = world.rank

        # set the source tasks
        source = 0
        # at the source task
        if rank == source:
            # say something
            print("Partitioner.partition:")
            print("    sample size: {}".format(sampleSize))
            print("    samples per task: {}".format(samplesPerTask))
            print("    number of tasks: {}".format(tasks))

            # allocate the source matrix
            θ = gsl.matrix(shape=(tasks*samplesPerTask, sampleSize))
            # initialize it
            for task in range(tasks):
                for sample in range(samplesPerTask):
                    for dof in range(sampleSize):
                        offset = task*samplesPerTask+sample 
                        θ[offset, dof] = (offset)*sampleSize+ dof
            # print it out
            θ.print(format="{}")
        # the other tasks
        else:
            # have a dummy source matrix
            θ = None

        # each task gets
        shape = (samplesPerTask, sampleSize)
        # time to scatter
        θ_n = scatter(matrix=θ, shape=shape, communicator=world, source=source)
        # print one of them out
        if rank == tasks//2: θ_n.print(format="{}")
            
        # all done
        return


    # meta-methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        return 


# end of file 
