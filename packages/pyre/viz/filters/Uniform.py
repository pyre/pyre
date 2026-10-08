# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Filter import Filter


# the filter that sorts a signal into bins of equal width
class Uniform(pyre.flow.factory, family="pyre.viz.filters.uniform", implements=Filter):
    """
    The filter that sorts the values of a signal into {bins} bins of equal width
    """

    # user configurable state
    bins = pyre.properties.int()
    bins.default = 10
    bins.doc = "the number of bins"

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal"

    # the output
    bin = pyre.viz.tile.output()
    bin.doc = "the bin of each sample"


# end of file
