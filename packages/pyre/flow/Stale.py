# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# support
import pyre


# declaration
class Stale:
    """
    A mix-in that remembers whether its client is stale or not
    """


    # public data
    @property
    def stale(self):
        """
        Return my current status
        """
        # easy enough
        return self._stale

    @stale.setter
    def stale(self, status):
        """
        Adjust my status
        """
        # if i'm being marked as stale
        if status is True:
            # flush
            return self.flush()
        # otherwise, just update the status
        self._stale = status
        # all done
        return self


    # meta-methods
    def __init__(self, stale, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my flag
        self._stale = stale
        # all done
        return


    # hooks
    def flush(self, **kwds):
        """
        Handler of the notification that the value of {observable} has changed
        """
        # update my state
        self._stale = True
        # chain up
        return super().flush(**kwds)


    # implementation details
    _stale = None


# end of file
