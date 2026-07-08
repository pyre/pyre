# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Device import Device


# a device that buffers entries while pyre is still booting
class BootDevice(Device):
    """
    A journal device used while pyre is still booting, before a real console can be built; it
    buffers entries and replays them once the framework hands journal a working device
    """

    # interface
    def alert(self, entry):
        """
        Buffer a user-facing alert for later replay
        """
        # remember the entry and the sink it should reach
        self.buffer.append(("alert", entry))
        # all done
        return self

    def help(self, entry):
        """
        Buffer a help screen for later replay
        """
        # remember the entry and the sink it should reach
        self.buffer.append(("help", entry))
        # all done
        return self

    def memo(self, entry):
        """
        Buffer a developer-facing memo for later replay
        """
        # remember the entry and the sink it should reach
        self.buffer.append(("memo", entry))
        # all done
        return self

    def replay(self, device):
        """
        Replay everything buffered into {device}, in the order it arrived, then forget it
        """
        # walk the buffered entries in arrival order
        for sink, entry in self.buffer:
            # send each one to its matching sink on the real device
            getattr(device, sink)(entry=entry)
        # the buffer has been drained
        self.buffer = []
        # hand back the device we replayed into
        return device

    # metamethods
    def __init__(self, name="boot", **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # the entries collected while the framework is still coming up
        self.buffer = []
        # all done
        return


# end of file
