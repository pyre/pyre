# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections
import os

# support
import pyre

# my superclass
from .Executive import Executive


# declaration
class Fork(Executive, family="pyre.shells.fork"):
    """
    A shell that invokes the main application behavior in a child process
    """

    # types
    # the channels that carry the standard streams of the child, one per stream
    streams = collections.namedtuple("streams", ["stdin", "stdout", "stderr"])

    # public state
    capture = pyre.properties.bool(default=True)
    capture.doc = "control whether to create communication channels to the daemon process"

    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the {application} behavior in a subprocess; both processes get the channels that
        carry the standard streams of the child, one per stream
        """
        # if we are in debug mode, launch the application
        if application.DEBUG:
            # in this process
            return application.main(*args, **kwds)

        # build the three pipes
        pipes = self.openCommunicationPipes()
        # and fork
        pid = os.fork()

        # in the parent process
        if pid > 0:
            # build and return the parent side channels
            channels = self.parentChannels(pipes)
            # invoke the parent behavior
            status = application.launched(*args, channels=channels, **kwds)
            # and return its status
            return status

        # in the child process, build the child side channels
        channels = self.childChannels(pipes)
        # set up a net
        try:
            # launch the application
            status = application.main(*args, channels=channels, **kwds)
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
        # and exit
        raise SystemExit(status)

    # implementation details
    def openCommunicationPipes(self):
        """
        Build three pipes for parent/child communication
        """
        # bail out if we are not supposed to build pipes to the child
        if not self.capture:
            # by building none
            return (None, None, None)

        # otherwise, build the pipes
        stdin = os.pipe()
        # one for each
        stdout = os.pipe()
        # standard stream
        stderr = os.pipe()
        # and return them
        return (stdin, stdout, stderr)

    def parentChannels(self, pipes):
        """
        Build the parent side of the communication channels: one that writes to the {stdin} of
        the child, and two that read its {stdout} and {stderr}
        """
        # bail out if we are not supposed to build pipes to the child
        if not self.capture:
            # with no channels
            return self.streams(stdin=None, stdout=None, stderr=None)

        # otherwise, access the pipe transport
        import pyre.ipc

        # instantiate it
        transport = pyre.ipc.newPipe()
        # unpack
        stdin, stdout, stderr = pipes
        # the ends the child uses are not mine
        for descriptor in (stdin[0], stdout[1], stderr[1]):
            # so close them, so that i see the end of its output when it exits
            os.close(descriptor)
        # make a channel for each stream, from the end i use
        return self.streams(
            stdin=transport.wrap(outfd=stdin[1]),
            stdout=transport.wrap(infd=stdout[0]),
            stderr=transport.wrap(infd=stderr[0]),
        )

    def childChannels(self, pipes):
        """
        Build the child side of the communication channels: one that reads its {stdin}, and two
        that write its {stdout} and {stderr}
        """
        # bail out if we are not supposed to build pipes to the child
        if not self.capture:
            # with no channels
            return self.streams(stdin=None, stdout=None, stderr=None)

        # otherwise, access the pipe transport
        import pyre.ipc

        # instantiate it
        transport = pyre.ipc.newPipe()
        # unpack
        stdin, stdout, stderr = pipes
        # the ends the parent uses are not mine
        for descriptor in (stdin[1], stdout[0], stderr[0]):
            # so close them, so that i see the end of my input when the parent is done with it
            os.close(descriptor)
        # make a channel for each stream, from the end i use
        return self.streams(
            stdin=transport.wrap(infd=stdin[0]),
            stdout=transport.wrap(outfd=stdout[1]),
            stderr=transport.wrap(outfd=stderr[1]),
        )


# end of file
