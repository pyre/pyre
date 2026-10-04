# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Filter import Filter


# the filter that maps the phase of a complex signal onto an interval
class Cycle(pyre.flow.factory, family="pyre.viz.filters.cycle", implements=Filter):
    """
    The filter that measures the phase of each sample of a complex signal as a fraction of a
    full turn, in [0,1), and maps it onto its {interval}
    """

    # user configurable state
    interval = pyre.properties.tuple(schema=pyre.properties.float(), default=(0, 1))
    interval.doc = "the interval that a full turn maps onto"

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal, a stream of complex values"

    # the output
    cycle = pyre.viz.tile.output()
    cycle.doc = "the phase of each sample, mapped onto {interval}"


# end of file
