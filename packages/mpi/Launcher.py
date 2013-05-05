# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import sys
import pyre
from pyre.shells.Executive import Executive # my superclass


# declaration
class Launcher(Executive, family='mpi.shells.mpirun'):
    """
    Encapsulation of launching an MPI job using {mpirun}
    """


    # user configurable state
    tasks = pyre.properties.int()
    tasks.doc = 'the number of mpi tasks'

    autospawn = pyre.properties.bool(default=True)
    autospawn.doc = 'set to {True} to re-launch this script under {mpirun}'

    # a marker that enables applications to deduce the type of shell that is hosting them
    model = pyre.properties.str(default='mpi')
    model.doc = "the programming model"


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Launch {application} as a collection of mpi tasks
        """
        # if we need to invoke {mpirun}
        if self.autospawn:
            # do it
            return self.spawn()

        # otherwise, just launch the application
        return self.main(application, *args, **kwds)


    # launching hooks; subclasses may override this to get finer control over the two launching
    # branches
    def main(self, application, *args, **kwds):
        """
        Called after the parallel machine has been built and it is time to invoke the user's
        code in every node
        """
        # launch the application and return its exit code
        return application.main(*args, **kwds)


    def spawn(self):
        """
        Invoke {mpirun} with the correct arguments to create the  parallel machine
        """
        # externals
        import subprocess

        # figure out which mpi we are using
        mpi = self.pyre_externals.locate(category='mpi')
        launcher = mpi.launcher
        # and which python
        python = self.pyre_externals.locate(category='python')
        interpreter = python.interpreter

        # NYI: check these and raise some exceptions if they are no good

        # start building the command line
        argv = [launcher]

        # if the user specified the number of tasks explicitly
        if self.tasks:
            # add the corresponding command line argument to the pile
            argv += ['-np', str(self.tasks)]

        # add python, the command line arguments to this script, and the autospawn marker
        argv += [interpreter] + sys.argv + ['--{.pyre_name}.autospawn=no'.format(self)]
        
        # set the subprocess options
        options = {
            'args': argv,
            'executable': launcher,
            #'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
            }

        # display the options
        # import pyre.tracking
        # print(' * {}: mpi.Launcher: subprocess options:'.format(pyre.tracking.here()))
        # for key,value in options.items(): print('    {} = {!r}'.format(key, value))

        # invoke {mpirun}
        with subprocess.Popen(**options) as child:
            # wait for it to finish
            status = child.wait()
        # and return its status
        return status


# end of file
