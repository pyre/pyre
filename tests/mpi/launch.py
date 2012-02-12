#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Launch an mpi application
"""


def test():
    import sys
    import mpi
    import pyre # access the framework

    # declare a trivial application
    class application(pyre.application, family='mpi.application'):
        """a sample application"""

        @pyre.export
        def main(self, **kwds):
            # get the world communicator
            world = mpi.world
            # print("Hello from {0.rank} of {0.size}".format(world)) 
            assert world.size == 8
            assert world.rank in range(world.size)
            return 0

    # instantiate it
    app = application(name=sys.platform)
    # run it
    app.run()

    # return the app
    return app


# main
if __name__ == "__main__":
    test()


# end of file 
