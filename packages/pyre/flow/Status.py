# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# support
import pyre


# declaration
class Status(pyre.tracker):
    """
    A helper that watches over a component's traits and records value changes
    """


    # public data
    raw = True


    # meta-methods
    def __init__(self, raw=raw, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my flag
        self.raw = raw
        # all done
        return


    # hooks
    def flush(self, observable, **kwds):
        """
        Handler of the notification that the value of {observable} has changed
        """
        # mark me
        self.raw = True
        # chain up
        return super().flush(observable=observable, **kwds)


# end of file
