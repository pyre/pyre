# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class InfoZip:
    """
    Mixin with file metadata from {zip} archives
    """

    # meta methods
    def __init__(self, info, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the metadata
        self.info = info
        # all done
        return


# end of file
