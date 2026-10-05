# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Filter import Filter


# the filter that sorts a signal into bins whose widths grow geometrically
class Geometric(pyre.flow.factory, family="pyre.viz.filters.geometric", implements=Filter):
    """
    The filter that sorts the values of a signal into {bins} bins whose widths grow by
    {ratio} from one bin to the next; values below the first bin land in bin -1, values
    above the last in bin {bins}
    """

    # user configurable state
    bins = pyre.properties.int()
    bins.default = 10
    bins.doc = "the number of bins"
    ratio = pyre.properties.float()
    ratio.default = 2
    ratio.doc = "the ratio of the widths of neighboring bins"

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal"

    # the output
    bin = pyre.viz.tile.output()
    bin.doc = "the bin of each sample"


# end of file
