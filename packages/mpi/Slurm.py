# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# externals
import sys, subprocess
# the framework
import pyre
# my superclass
from .Launcher import Launcher


# declaration
class Slurm(Launcher, family='mpi.shells.slurm'):
    """
    Encapsulation of launching an MPI job using SLURM
    """


    # user configurable state
    sbatch = pyre.properties.path(default='sbatch')
    sbatch.doc = 'the path to the sbatch launcher'

    queue = pyre.properties.str()
    queue.doc = 'the name of the queue that will receive this job'

    submit = pyre.properties.bool(default=True)
    submit.doc = 'if {True} invoke sbatch; otherwise just save the SLURM script in a file'

    # spawning the application
    def spawn(self, application):
        """
        Generate a {SLURM} script and submit a job
        """
        # figure out which mpi we are using
        launcher = self.mpi.launcher
        # and which python
        interpreter = sys.executable

        # we have two things to build: the SLURM script, and the command line to {sbatch} to
        # submit the job to the queuing system

        # start building the command line that we will include in the SLURM script
        argv = [launcher]
        if self.tasks:
            # add the corresponding command line argument to the pile
            argv += ['-np', str(self.tasks)]
        # add python, the command line arguments to this script, and the autospawn marker
        argv += [interpreter] + sys.argv + ['--{.pyre_name}.autospawn=no'.format(self)]

        # here is the body of the script
        script = '\n'.join([
            '#!/bin/bash',
            '',
            '#SBATCH --job-name="{}"'.format(application.pyre_name),
            '#SBATCH --ntasks={}'.format(self.tasks),
            '#SBATCH --output="{}.out"'.format(application.pyre_name),
            '#SBATCH --error="{}.err"'.format(application.pyre_name),
            '#SBATCH --partition={}'.format(self.queue),
            '',
            '# load the environment',
            '[ -r /etc/profile ] && source /etc/profile',
            '',
            '# launch the pyre application',
            ' '.join(argv),
            '',
            '# end of file'
            ])

        # if we were asked not to invoke SLURM
        if not self.submit:
            # open a file named after the app
            with open(application.pyre_name+'.slurm', 'w') as record:
                # write the script
                record.write(script)
                # and return success
                return 0

        # grab the launcher
        sbatch = str(self.sbatch)
        # command line arguments
        options = {
            'args': [sbatch],
            'executable': sbatch,
            'stdin': subprocess.PIPE, 'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE,
            'universal_newlines': True,
            'shell': False
            }
        # invoke {sbatch}
        with subprocess.Popen(**options) as child:
            # send it the script
            response, errors = child.communicate(script)
            # if {sbatch} said anything
            if response: application.info.log(response)
            # if there was a problem
            if errors: application.error.log(errors)
            # wait for it to finish
            status = child.wait()
        # and return its status
        return status


# end of file
