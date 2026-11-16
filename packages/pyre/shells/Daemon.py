# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import sys

# support
import pyre

# my superclass
from .Fork import Fork


# declaration
class Daemon(Fork, family="pyre.shells.daemon"):
    """
    A shell that turns a process into a daemon, i.e. a process that is detached from its
    parent and has no access to a terminal
    """

    # user configurable state
    capture = pyre.properties.bool(default=False)  # to override the default from {Fork}
    capture.doc = "control whether to create communication channels to the daemon process"
    # a marker that enables applications to deduce the type of shell that is hosting them
    model = pyre.properties.str(default="daemon")
    model.doc = "the programming model"

    # whether i am the process that runs the application
    daemon = pyre.properties.bool(default=False)
    daemon.doc = "internal marker to indicate that the spawning is complete"

    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior

        For daemons, this is somewhat involved: the process forks twice in order to detach
        itself completely from its parent.
        """
        # if i was told not to spawn, just invoke the behavior
        if application.DEBUG:
            # in this process
            return application.main(*args, **kwds)

        # if spawning is done
        if self.daemon:
            # figure out where to park the process
            home = self.home or "/"
            # go there
            os.chdir(home)
            # set up a net
            try:
                # launch the application
                status = application.main(*args, **kwds)
            # if anything goes wrong
            except self.PyreError as error:
                # log it
                application.error.log(str(error))
                # set the status
                status = 1
            # if all went well
            else:
                # shutdown
                application.pyre_shutdown(status=status)
            # return the exit code
            raise SystemExit(status)

        # otherwise, build the communication channels
        pipes = self.openCommunicationPipes()
        # fork
        pid = os.fork()

        # in the parent process, build and return the parent side channels
        if pid > 0:
            # create the channels to the child
            channels = self.parentChannels(pipes)
            # invoke the parent behavior
            status = application.launched(*args, channels=channels, **kwds)
            # and return its status
            return status

        # in the intermediate child, decouple from the parent environment; don't change the
        # {cwd} just yet so {exec} below can find the script that launched the application
        os.setsid()
        # and from the permissions it would give the files it makes
        os.umask(0)

        # respawn
        pid = os.fork()

        # in the intermediate process
        if pid > 0:
            # exit immediately and unconditionally
            return os._exit(0)

        # in the final child process, build the channels to the launching process
        channels = self.childChannels(pipes)
        # if there are any
        if self.capture:
            # daemons use their standard streams to communicate with the launching process, so
            # install the channels in their place, where they survive the {exec}: the launching
            # process writes to my input
            channels.stdin.install(stream=0)
            # reads my output
            channels.stdout.install(stream=1)
            # and my error stream
            channels.stderr.install(stream=2)

        # build the command line
        argv = [sys.executable] + sys.argv + [f"--{self.pyre_name}.daemon=True"]

        # and try
        try:
            # to exec so that signals get delivered correctly
            os.execv(sys.executable, argv)
        # if the interpreter could not be started
        except OSError as error:
            # say so
            application.error.log(str(error))

        # all done
        return


# end of file
