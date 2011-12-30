# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

# access to os services
import os
# access to {exit}
import sys
# for the master-child communication
import pickle
# access to the framework
import pyre
# and the journal
import journal
# my superclass
from .Script import Script


# declaration
class Daemon(Script, family="pyre.shells.daemon"):
    """
    A shell that turns a process into a daemon, i.e. a process that is detached from its
    parent and has no access to a terminal
    """


    # utilities
    from . import proc


    # public data
    debug = pyre.properties.bool(default=False)
    debug.doc = "set to {True} to prevent the process from detaching from its parent"


    args = None # my invocation argument vector
    kwds = None # my invocation argument keywords
    pread = None
    pwrite = None

    
    # interface
    @pyre.export
    def run(self, *args, **kwds):
        """
        Invoke the application behavior

        For daemons, this is somewhat involved: the process forks twice in order to detach
        itself completely from its parent.
        """
        # save my arguments
        self.args = args
        self.kwds = kwds
        # if i was told not to spawn
        if self.debug:
            # log the fact
            journal.warning(self.pyre_name).log("daemon {.pyre_name!r} in debug mode".format(self))
            # and invoke the behavior
            return self.daemon(pid=0)

        # otherwise
        # open a communication channel
        self.pread, self.pwrite = os.pipe()
        # double fork
        return self.proc.fork(self.done, self.respawn)


    # implementation details
    def done(self, pid):
        """
        The behavior at the master process
        """
        status = pickle.loads(os.read(self.pread, 1024))
        # print("master: child reported pid={}".format(status))
        # just return the process id of the child
        return pid


    def respawn(self, pid):
        """
        The behavior at the intermediate process
        """
        journal.info(self.pyre_name).log("intermediate: {}: detaching...".format(pid))
        # decouple from the parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
        # respawn
        return self.proc.fork(self.exit, self.daemon)


    def exit(self, pid=None):
        """
        Terminate the intermediate process
        """
        journal.info(self.pyre_name).log("intermediate: child={}: exiting...".format(pid))
        # return successfully
        return sys.exit(0)


    def daemon(self, pid):
        """
        The behavior of the daemon process
        """
        journal.info(self.pyre_name).log("child: {}: launching...".format(pid))
        # check whether my {home} directory exists
        if not (self.home and os.path.exists(self.home)):
            # if not, log an error
            journal.error(self.pyre_name).log(
                "{}: home directory {.home!r} does not exist".format(pid, self))
            # and go to the temporary directory
            self.home = "/tmp"
        # change the working directory to my {home}
        os.chdir(self.home)
        journal.info(self.pyre_name).log("child: {}: at {!r}".format(pid, os.getcwd()))

        # send my pid to my parent
        os.write(self.pwrite, pickle.dumps({'pid': pid}))

        # if i don't have an application object
        if self.application is None:
            # there's nothing further to do
            return 0
        # if we are in debug mode
        if self.debug:
            # invoke the application {main}
            return self.application.main(*self.args, **self.kwds)

        # otherwise, close all ties with the parent process
        os.close(2)
        os.close(1)
        os.close(0)
        # launch the application
        try:
            return self.application.main(*self.args, **self.kwds)
        # if anything goes wrong
        except Exception as error:
            # access the exception formatting package
            import traceback
            # log an error
            journal.error(self.pyre_name).log(
                "exception:\n {}".format(traceback.format_exc()))
        # and return with an error code
        return 1


# end of file 
