#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


"""
Launch an mpi application
"""

# the driver
def test():
    # access the framework
    import pyre

    # declare a trivial application
    class application(pyre.application, family='mpi.application'):
        """a sample application"""

        @pyre.export
        def main(self, **kwds):
            # get the mpi support
            import mpi
            # get the world communicator
            world = mpi.world
            # check
            assert world.size == self.shell.tasks
            assert world.rank in range(world.size)
            # all done
            return 0

    # instantiate it
    app = application(name='mpirun')
    # run it
    status = app.run()
    # check
    assert status == 0
    # and return the app
    return app


# bootstrap
if __name__ == "__main__":
    # do it...
    test()


# end of file
