# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections


# a log of the values keys have taken
class Tracker:
    """
    Record the values a key has taken
    """

    # interface
    def getHistory(self, key: object) -> list:
        """
        Retrieve the historical record associated with a particular {key}
        """
        # look it up without leaving an empty record behind for keys that were never tracked
        return self.log.get(key, [])

    def track(self, key: object, node: object) -> None:
        """
        Add {node} to the history of {key}
        """
        # append it to the record
        self.log[key].append(node)
        # all done
        return

    # meta methods
    def __init__(self, **kwds) -> None:
        """
        Start with an empty log
        """
        # chain up
        super().__init__(**kwds)
        # the index of historical values
        self.log = collections.defaultdict(list)
        # all done
        return


# end of file
