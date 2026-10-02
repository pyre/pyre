# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# shared channel state
class Inventory:
    """
    Settings that are shared by all channels of the same name and severity
    """

    # interface
    def copy(self, source):
        """
        Make me look like {source}
        """
        # make a copy
        self.active = source.active
        self.fatal = source.fatal
        self.device = source.device
        # all done
        return

    # metamethods
    def __init__(self, active=True, fatal=False, device=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the activation state of the channel
        self.active = active
        # fatal channels raise exceptions on output
        self.fatal = fatal
        # the custom output device; {None} defers to the severity wide default
        self.device = device
        # all done
        return


# end of file
