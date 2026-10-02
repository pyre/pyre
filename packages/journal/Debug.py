# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os

# superclass
from .Channel import Channel

# the parsing rules for the environment
from .Chronicler import Chronicler

# the index, and the inventories it holds
from .Index import Index
from .Inventory import Inventory


# the implementation of the debug channel
class Debug(Channel, active=False, fatal=False):
    """
    Debug channels are used for communicating application progress to developers
    """

    # types
    from .exceptions import DebugError

    # implementation details
    @classmethod
    def initializeIndex(cls, active: bool, fatal: bool):
        """
        Build my index, with the channels named in the {JOURNAL_DEBUG} environment variable active
        """
        # make an index with my default state
        index = Index(active=active, fatal=fatal)
        # read the environment variable
        names = os.environ.get("JOURNAL_DEBUG")
        # if it's not there
        if names is None:
            # the index is empty
            return index
        # go through the names it lists
        for name in Chronicler.nameset(text=names):
            # and start each one out active and non fatal
            index[name] = Inventory(active=True, fatal=False)
        # all done
        return index

    def record(self):
        """
        Make an entry in the journal
        """
        # hunt down my device and record the entry
        self.device.memo(entry=self.entry)
        # all done
        return self

    # constants
    severity = "debug"  # the channel severity
    headline = "debug"  # the summary of the condition when i'm fatal
    fatalError = DebugError  # the exception i raise when i'm fatal


# end of file
