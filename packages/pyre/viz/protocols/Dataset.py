# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# the protocol of one of the datasets in a file
class Dataset(pyre.flow.specification, family="pyre.viz.datasets"):
    """
    One of the datasets in a file, known by its value along every axis of the file's contents,
    which hands the cells it holds to whatever cuts tiles out of them
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default way of holding a dataset
        """
        # in memory
        from ..datasets.Memory import Memory

        # publish
        return Memory


# end of file
