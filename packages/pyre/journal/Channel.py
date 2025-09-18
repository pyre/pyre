# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import pyre
import journal


# the base channel manager
class Channel(pyre.component, family="pyre.journal.channel"):
    """
    The manager of an application journal channel
    """

    # constants
    severity = "info"  # subclasses should override

    # user configurable state
    active = pyre.properties.bool()
    active.default = True
    active.doc = "control whether the channel produces output"

    fatal = pyre.properties.bool()
    fatal.default = False
    fatal.doc = "control whether the channel produces output"

    # metamethods
    def __init__(self, section, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the channel name
        self.section = section
        # all done
        return

    # framework hooks
    def apply(self):
        """
        Transfer my state to the journal
        """
        # get the channel factory
        factory = getattr(journal, self.severity)
        # build the channel
        channel = factory(name=self.section)
        # transfer my state
        channel.active = self.active
        channel.fatal = self.fatal
        # all done
        return


# end of file
