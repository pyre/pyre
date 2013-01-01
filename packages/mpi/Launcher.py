# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the path to the mpi launcher'

    python = pyre.properties.str(default=sys.executable)
    python.doc = 'the path to the interpreter'

    tasks = pyre.properties.int()
    tasks.doc = 'the number of mpi tasks'


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Launch {application} as a collection of mpi tasks
        """

        # check whether the mpi tasks have already been spawned
        if self.pyre_executive.nameserver.get('with-mpi', False):
            # launch the application
            status = application.main_mpi(*args, **kwds)
            # and exit
            return sys.exit(status)

        # build the command line
        argv = [
            self.launcher,
            '-np', str(self.tasks),
            self.python ] + sys.argv + [
            '--with-mpi=true',
            ]
        # set the subprocess options
        options = {
            'args': argv,
            'executable': self.launcher,
            # 'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
            }

        # display the options
        # import pyre.tracking
        # print(' * {}: mpi.Launcher: subprocess options:'.format(pyre.tracking.here()))
        # for key,value in options.items(): print('    {} = {!r}'.format(key, value))
        # make a pipe
        with subprocess.Popen(**options) as child:
            # wait for it to finish
            status = child.wait()
        # and return its status
        return status


# end of file
