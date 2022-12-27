# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# shared channel state
class Inventory:
    """
    Settings that are shared by all channels of the same name and severity
    """


    # public data
    active = None  # the activation state of the channel
    fatal = None   # fatal channels raise exceptions on output
    device = None  # the custom output device


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


# end of file
