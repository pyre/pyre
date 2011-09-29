# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Memo:
    """
    A mix-in class that implements value memoization
    """


    # public data
    @property
    def value(self):
        """
        Override the node value retriever and return the contents of my value cache if it is up
        to date; otherwise, recompute the value and update the cache
        """
        # if my cache is invalid
        if self._value is None:
            # recompute
            self._value = super().value
        # return the cache contents
        return self._value


    # private data
    _value = None


# end of file 
