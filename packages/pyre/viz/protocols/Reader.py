# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the specifications of my slots
from .Datasets import Datasets


# the protocol of the factories that open files
class Reader(pyre.flow.producer, family="pyre.viz.readers"):
    """
    The reader protocol: open a file and make its datasets available to the selectors that pick
    the one to look at
    """

    # the output
    datasets = Datasets.output()
    datasets.doc = "the datasets in the file"


# end of file
