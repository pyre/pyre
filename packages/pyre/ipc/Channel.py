# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# leif strand
# (c) 1998-2026 all rights reserved


# externals
import os
import fcntl


# declaration
class Channel:
    """
    A wrapper around the lower level IPC mechanisms that normalizes the sending and receiving
    of messages. See {Pipe} and {Socket} for concrete examples of encapsulation of the
    operating system services.
    """

    # interface
    # channel life cycle management
    @classmethod
    def open(cls, **kwds):
        """
        Channel factory
        """
        raise NotImplementedError(f"class '{cls.__name__}' must implement 'open'")

    # access to the individual channel end points
    @property
    def inbound(self):
        """
        Retrieve the channel end point that can be read
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'inbound'"
        )

    @property
    def outbound(self):
        """
        Retrieve the channel end point that can be written
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'outbound'"
        )

    # input/output
    def read(self, minlen, maxlen):
        """
        Read up to {maxlen} bytes from my input channel
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'read'"
        )

    def write(self, bytes):
        """
        Write the {bytes} to the output channel
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'write'"
        )

    def close(self):
        """
        Shutdown the channel
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'close'"
        )

    # support
    @staticmethod
    def clearCLOEXEC(fd):
        """
        Clear the FD_CLOEXEC bit of {fd} to make sure it not inherited by child processes
        created with the {exec} family of spawners
        """
        # get the current flags
        flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        # clear the CLOEXEC bit
        flags &= ~fcntl.FD_CLOEXEC
        # and update the file descriptor
        fcntl.fcntl(fd, fcntl.F_SETFD, flags)
        # all done
        return

    @staticmethod
    def setCLOEXEC(fd):
        """
        Set the FD_CLOEXEC bit of {fd} to make sure it is not inherited by child processes
        created with the {exec} family of spawners
        """
        # get the current flags
        flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        # set the CLOEXEC bit
        flags |= fcntl.FD_CLOEXEC
        # and update the file descriptor
        fcntl.fcntl(fd, fcntl.F_SETFD, flags)
        # all done
        return

    @staticmethod
    def openFileDescriptors():
        """
        Generate a sequence of open file descriptors
        """
        # set up a pile of names
        names = []
        # macos and linux place the file descriptors in different places
        for path in ("/proc/self/fd", "/dev/fd"):
            # carefully
            try:
                # to list the directory contents
                names.extend(os.listdir(path))
            # if the {path} doesn't exist
            except FileNotFoundError:
                # ignore and move on
                pass
        # now, go through the names, pick out the ones that are numbers and hand them off
        yield from (name for name in names if name.isdigit())
        # all done
        return


# end of file
