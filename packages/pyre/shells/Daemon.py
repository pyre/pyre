# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import os # access to os services
import pyre # access the framework
from .Fork import Fork # my superclass


# declaration
class Daemon(Fork, family="pyre.shells.daemon"):
    """
    A shell that turns a process into a daemon, i.e. a process that is detached from its
    parent and has no access to a terminal
    """


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior

        For daemons, this is somewhat involved: the process forks twice in order to detach
        itself completely from its parent.
        """
        # if i was told not to spawn
        if self.debug:
            # log the fact
            self._warning.log("daemon: {.pyre_name!r}: in debug mode".format(self))
            # and invoke the behavior
            return application.main(*args, **kwds)

        # otherwise, build the communication channels
        channels = self.channels()
        # fork
        pid = os.fork()

        # in the parent process
        if pid > 0:
            # notify
            self._debug.log("    in the parent process: resuming")
            # build and return the parent side channels
            return self.parentChannels(channels)

        # in the intermediate child, decouple from the parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # respawn
        pid = os.fork()

        # in the intermediate process, just exit
        if pid > 0: return os._exit(0)

        # in the final child process, convert {stdout} and {stderr} into channels
        stdout, stderr = self.childChannels(channels)
        # launch the application
        status = application.main(*args, stdout=stdout, stderr=stderr, **kwds)
        # and exit
        return os._exit(status)


# end of file 
