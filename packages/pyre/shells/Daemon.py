# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import os # access to os services
import sys
import pyre # access the framework
from .Fork import Fork # my superclass


# declaration
class Daemon(Fork, family="pyre.shells.daemon"):
    """
    A shell that turns a process into a daemon, i.e. a process that is detached from its
    parent and has no access to a terminal
    """

   
    # user configurable state
    capture = pyre.properties.bool(default=False) # to override the default from {Fork}
    capture.doc = "control whether to create communication channels to the daemon process"
    # a marker that enables applications to deduce the type of shell that is hosting them
    model = pyre.properties.str(default='daemon')
    model.doc = "the programming model"


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior

        For daemons, this is somewhat involved: the process forks twice in order to detach
        itself completely from its parent.
        """
        # if i was told not to spawn, just invoke the behavior
        if self.debug: return application.main(*args, **kwds)

        # otherwise, build the communication channels
        pipes = self.openCommunicationPipes()
        # fork
        pid = os.fork()

        # in the parent process, build and return the parent side channels
        if pid > 0: return self.parentChannels(pipes)

        # in the intermediate child, decouple from the parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # respawn
        pid = os.fork()

        # in the intermediate process, just exit
        if pid > 0: return os._exit(0)

        # in the final child process, convert {stdout} and {stderr} into channels
        channels = self.childChannels(pipes)
        # if the user has specified a home directory for this process, go there
        if self.home: os.chdir(self.home)
        # launch the application and return its exit code
        return application.main(*args, channels=channels, **kwds)


# end of file 
