# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import collections


# class declaration
class Tracker:
    """
    Record the values a key has taken
    """


    def getHistory(self, key):
        """
        Retrieve the historical record associated with a particular {key}
        """
        return self.log[key]


    def track(self, key, value):
        """
        Add {value} to the history of {key}
        """
        self.log[key].append(value)
        return


    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.log = collections.defaultdict(list)

        return


# end of file
