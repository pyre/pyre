# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections
import fcntl
import functools
import importlib
import os
import select

# the exceptions raised by channels
from .exceptions import CarriageError, ChannelError, TravelError


# declaration
class Channel:
    """
    A wrapper around the lower level IPC mechanisms that normalizes the sending and receiving
    of messages. See {Pipe} and {Socket} for concrete examples of encapsulation of the
    operating system services.

    The ends of a channel are descriptors. A channel can travel to another process, in a
    message or across an {exec}: it says how it leaves, as its hints and the descriptors it is
    made of, and its class rebuilds it on arrival from the hints and the descriptors that came
    with them. The hints name the class by its import path, so channels of any kind can travel
    """

    # types
    # the pair of connected endpoints handed out by channel factories; the {parent} end stays
    # with the process that built the pair and does not survive an {exec}, while the {child}
    # end is inheritable, destined for the other party of the conversation
    ends = collections.namedtuple("ends", ["parent", "child"])

    # interface
    # channel life cycle management
    @classmethod
    def open(cls, **kwds):
        """
        Channel factory
        """
        # every kind of channel knows how to make itself
        raise NotImplementedError(f"class '{cls.__name__}' must implement 'open'")

    # access to the individual channel end points
    @property
    def inbound(self) -> int | None:
        """
        Retrieve the descriptor of the channel end point that can be read
        """
        # every kind of channel knows its ends
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'inbound'")

    @property
    def outbound(self) -> int | None:
        """
        Retrieve the descriptor of the channel end point that can be written
        """
        # every kind of channel knows its ends
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'outbound'")

    def descriptors(self) -> list[int]:
        """
        The descriptors i am made of, in the order my class rebuilds me from them
        """
        # every kind of channel knows what it is made of
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'descriptors'")

    # input/output
    def read(self, minlen, maxlen):
        """
        Read up to {maxlen} bytes from my input channel
        """
        # every kind of channel knows how to read
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'read'")

    def pending(self) -> bool:
        """
        Check, without waiting, whether a read would find something: bytes, or the end of the
        stream
        """
        # a channel that cannot be read has nothing waiting
        if self.inbound is None:
            # so say so
            return False
        # make a poller
        poller = select.poll()
        # interested in the end i read from
        poller.register(self.inbound, select.POLLIN)
        # and ask it without waiting; a peer that hung up counts, since a read then finds the
        # end of the stream
        return bool(poller.poll(0))

    def write(self, bytes, descriptors=()):
        """
        Write the {bytes} to the output channel, along with the open file {descriptors}, if any
        """
        # every kind of channel knows how to write
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'write'")

    def claim(self, count: int) -> list[int]:
        """
        Take the {count} descriptors that arrived with the bytes just read
        """
        # a channel that cannot carry descriptors has none to give
        if count:
            # so asking for some is a mistake
            raise CarriageError(channel=self, reason="it cannot receive open descriptors")
        # otherwise, there is nothing to hand over
        return []

    def close(self):
        """
        Shutdown the channel
        """
        # every kind of channel knows how to release its descriptors
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'close'")

    # control
    def setBlocking(self, flag: bool) -> "Channel":
        """
        Make reading and writing wait, or not, according to {flag}
        """
        # go through my descriptors
        for descriptor in self.descriptors():
            # and set each one
            os.set_blocking(descriptor, flag)
        # all done
        return self

    def install(self, stream: int) -> "Channel":
        """
        Make me the standard {stream} of this process, by its descriptor number: {0} for its
        input, {1} for its output, {2} for its error stream; the stream survives an {exec}
        """
        # standard input is read, the others are written
        end = self.inbound if stream == 0 else self.outbound
        # put my end in its place; the copy is inheritable
        os.dup2(end, stream)
        # all done
        return self

    # travel
    def depart(self) -> tuple[dict[str, str], list[int]]:
        """
        Describe how i leave this process: my hints, which name my class and carry whatever else
        it needs to rebuild me, and the descriptors i am made of
        """
        # my class
        kind = type(self)
        # named by its import path
        hints = {"kind": f"{kind.__module__}:{kind.__qualname__}"}
        # along with what it needs to know about me
        hints.update(self.hints())
        # and my descriptors
        return hints, self.descriptors()

    @classmethod
    def arrive(cls, hints: dict[str, str], descriptors: list[int]) -> "Channel":
        """
        Rebuild the channel described by {hints} from the {descriptors} that arrived with them
        """
        # split the name of the class into its module and its name within the module
        module, _, name = hints["kind"].partition(":")
        # carefully
        try:
            # find the class
            kind = functools.reduce(getattr, name.split("."), importlib.import_module(module))
        # if the module or the class are not there
        except (ImportError, AttributeError) as error:
            # the channel cannot be rebuilt here
            raise TravelError(hints=hints, reason=str(error)) from error
        # if what was found is not a channel class
        if not isinstance(kind, type) or not issubclass(kind, Channel):
            # it cannot rebuild a channel either
            raise TravelError(hints=hints, reason="it does not name a kind of channel")
        # otherwise, let it rebuild the channel
        return kind.rebuild(hints=hints, descriptors=descriptors)

    # travel hooks for my subclasses
    def hints(self) -> dict[str, str]:
        """
        What my class needs to know, beyond my descriptors, to rebuild me
        """
        # nothing, by default
        return {}

    @classmethod
    def rebuild(cls, hints: dict[str, str], descriptors: list[int]) -> "Channel":
        """
        Build one of my instances from its {hints} and its {descriptors}
        """
        # every kind of channel knows how to rebuild itself
        raise NotImplementedError(f"class '{cls.__name__}' must implement 'rebuild'")

    # metamethods
    def __reduce_ex__(self, protocol):
        """
        Refuse to be pickled, or copied, outside a marshaler: my descriptors are numbers that
        mean something only in this process, so i travel only inside a marshaled message,
        which carries the descriptors themselves
        """
        # complain
        raise ChannelError(channel=self)

    # support
    @staticmethod
    def clearCLOEXEC(fd):
        """
        Clear the FD_CLOEXEC bit of {fd}, so that it is inherited by child processes created
        with the {exec} family of spawners
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
