#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


"""
Launch an mpi application
"""


def test():
    # access the framework
    import pyre

    # declare a trivial application
    class application(pyre.application, family='mpi.application'):
        """a sample application"""

        @pyre.export
        def main(self, **kwds):
            # access the package
            import mpi
            # get the world communicator
            world = mpi.world
            print("Hello from {0.rank} of {0.size}".format(world))
            # check
            # assert world.size == 8
            # assert world.rank in range(world.size)
            # all done
            return 0

    # instantiate it
    app = application(name='slurm')
    # run it
    app.run()

    # return the app
    return app


# main
if __name__ == "__main__":
    test()


# end of file
