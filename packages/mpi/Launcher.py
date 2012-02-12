# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import sys
import pyre
import subprocess
from pyre.shells.Executive import Executive # my superclass


# declaration
class Launcher(Executive, family='mpi.shells.mpirun'):
    """
    Encapsulation of launching an MPI job using {mpirun}
    """


    # public state
    command = pyre.properties.str(default='mpirun')
    command.doc = 'the path to the mpi launcher'

    tasks = pyre.properties.int()
    tasks.doc = 'the number of mpi tasks'


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Launch {application} as a collection of mpi tasks
        """

        # check whether the mpi tasks have already been spawned
        if self.pyre_executive.configurator.get('worker', False):
            # launch the application
            status = application.main(*args, **kwds)
            # and exit
            return sys.exit(status)

        # otherwise, access the __main__ module
        import __main__

        # build the command line
        argv = [
            self.command,
            '-np', str(self.tasks),
            sys.executable,
            __main__.__file__,
            '--worker=true',
            ]
        # the options
        options = {
            'args': argv,
            'executable': self.command,
            # 'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
            }

        # make a pipe
        with subprocess.Popen(**options) as child:
            # wait for it to finish
            status = child.wait()
        # and return its status
        return status
            

# end of file 
