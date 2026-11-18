# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import mmap
import os
import tempfile

# base class
from .Channel import Channel

# exceptions
from .exceptions import CarriageError


# declaration
class File(Channel):
    """
    A channel over an open file

    The channel owns its descriptor, which it reads from and writes to, so its inbound and
    outbound ends are the same. It travels like every other channel, and arrives as a copy of
    the descriptor that refers to the same open file. Clients reach the file through the
    channel: they {share} it as a python file object of their own, {map} it, and {close} it
    """

    # factories
    @classmethod
    def open(cls, *, path, flags: int = os.O_RDONLY, permissions: int = 0o600, **kwds) -> "File":
        """
        Open the file at {path} with the given {flags}, creating it with the given
        {permissions} when the {flags} ask for it
        """
        # open the file; the descriptor is not inherited by processes made by {exec}
        descriptor = os.open(str(path), flags, permissions)
        # and wrap it
        return cls(descriptor=descriptor, **kwds)

    @classmethod
    def temporary(cls, *, folder=None, **kwds) -> "File":
        """
        Make a file with no name, in {folder} or in the standard place for temporary files,
        whose storage is reclaimed when the last descriptor that refers to it is closed
        """
        # make a temporary file
        descriptor, path = tempfile.mkstemp(dir=None if folder is None else str(folder))
        # and remove its name, so that only its descriptors keep it alive
        os.unlink(path)
        # wrap it
        return cls(descriptor=descriptor, **kwds)

    # access to the file
    def share(self, mode: str = "rb"):
        """
        Hand out a python file object of its own over my file, opened in {mode}; it refers to
        the same open file, including its position, and stays open after i am closed
        """
        # duplicate my descriptor and dress it up as a file object
        return os.fdopen(os.dup(self.descriptor), mode)

    def map(self, size: int | None = None, access: int = mmap.ACCESS_READ) -> mmap.mmap:
        """
        Map the first {size} bytes of my file, or all of it when {size} is not set, with the
        given {access}
        """
        # an unset size asks the kernel for the whole file
        length = 0 if size is None else size
        # map it
        return mmap.mmap(self.descriptor, length, access=access)

    # life cycle management
    def close(self):
        """
        Release my descriptor; the file itself lives on as long as other descriptors refer to it
        """
        # if i still have my descriptor
        if self.descriptor is not None:
            # close it
            os.close(self.descriptor)
            # and forget it, so it is never closed twice
            self.descriptor = None
        # all done
        return

    # access to the individual channel end points
    @property
    def inbound(self) -> int | None:
        """
        Retrieve the descriptor of the channel end point that can be read
        """
        # i read from my file
        return self.descriptor

    @property
    def outbound(self) -> int | None:
        """
        Retrieve the descriptor of the channel end point that can be written
        """
        # and write to the same file
        return self.descriptor

    def descriptors(self) -> list[int]:
        """
        The descriptors i am made of: the one over my file, while i have it
        """
        # easy enough
        return [] if self.descriptor is None else [self.descriptor]

    # input/output
    def read(self, minlen: int = 0, maxlen: int = 64 * 1024) -> bytes:
        """
        Read at least {minlen} and at most {maxlen} bytes from the current position in my file,
        or whatever is there before its end
        """
        # make sure
        if maxlen < minlen:
            # that the limits are sane
            maxlen = minlen
        # reset the byte count
        total = 0
        # initialize the packet pile
        packets = []
        # for as long as it takes
        while True:
            # pull something from the file
            packet = os.read(self.descriptor, maxlen - total)
            # get its length
            got = len(packet)
            # if we got nothing, we are at the end of the file
            if got == 0:
                # bail
                break
            # otherwise, update the total
            total += got
            # and save the packet
            packets.append(packet)
            # if we have reached our goal
            if total >= minlen:
                # bail
                break
        # assemble the byte string and return it
        return b"".join(packets)

    def write(self, bytes: bytes, descriptors=()) -> int:
        """
        Write all of {bytes} at the current position in my file; files cannot carry open
        {descriptors}
        """
        # if i am asked to carry descriptors
        if descriptors:
            # refuse
            raise CarriageError(channel=self, reason="files hold bytes only")
        # get a view of the bytes, so the remainder can be written without copies
        remainder = memoryview(bytes)
        # until they are all written
        while remainder:
            # write what the file takes
            written = os.write(self.descriptor, remainder)
            # and move on to the rest
            remainder = remainder[written:]
        # report the number of bytes written
        return len(bytes)

    # travel
    @classmethod
    def rebuild(cls, hints, descriptors) -> "File":
        """
        Build a file channel from its {hints} and its {descriptors}
        """
        # get my descriptor
        (descriptor,) = descriptors
        # and build the channel around it
        return cls(descriptor=descriptor)

    # meta methods
    def __init__(self, descriptor: int, **kwds):
        # chain up
        super().__init__(**kwds)
        # the descriptor over my file, which is mine to close
        self.descriptor = descriptor
        # all done
        return

    def __str__(self):
        # build a human readable representation
        return f"file at fd {self.descriptor}"


# end of file
