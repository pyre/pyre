# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import collections


# keeper of the historical values of a {key}
class Tracker:
    """
    Record the values a key has taken
    """


    def getHistory(self, key):
        """
        Retrieve the historical record associated with a particular {key}
        """
        # look up the {key} in my log and return the list of historical values
        return self.log[key]


    def track(self, key, node):
        """
        Add {node} to the history of {key}
        """
        # place {node} in the {key} pile
        self.log[key].append(node)
        # all done
        return


    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the index of historical values
        self.log = collections.defaultdict(list)
        # all done
        return


# end of file
