# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Device import Device


# a device that forwards every entry it receives to each of the devices attached to it
class Splitter(Device):
    """
    Journal device that forwards every entry to each of the devices attached to it
    """

    # constants
    name = "splitter"

    # interface
    def attach(self, device):
        """
        Add {device} to the set i forward to
        """
        # add it to the pile
        self.outputs.append(device)
        # and enable chaining
        return self

    def alert(self, entry):
        """
        Generate an alert
        """
        # go through my devices
        for output in self.outputs:
            # and hand each one the entry
            output.alert(entry)
        # all done
        return self

    def help(self, entry):
        """
        Generate a help screen
        """
        # go through my devices
        for output in self.outputs:
            # and hand each one the entry
            output.help(entry)
        # all done
        return self

    def memo(self, entry):
        """
        Generate a memo
        """
        # go through my devices
        for output in self.outputs:
            # and hand each one the entry
            output.memo(entry)
        # all done
        return self

    # metamethods
    def __init__(self, outputs=(), name=name, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # the devices i forward to, in the order they were attached
        self.outputs = list(outputs)
        # all done
        return


# end of file
