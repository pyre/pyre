# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Filter import Filter


# the filter that maps an interval onto [0,1]
class Parametric(pyre.flow.factory, family="pyre.viz.filters.parametric", implements=Filter):
    """
    The filter that maps the values of a signal in its {interval} onto [0,1], the way the
    colormaps expect them
    """

    # user configurable state
    interval = pyre.properties.tuple(schema=pyre.properties.float(), default=(0, 1))
    interval.doc = "the range of values that maps onto [0,1]"

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal"

    # the output
    parametric = pyre.viz.tile.output()
    parametric.doc = "the signal with its {interval} mapped onto [0,1]"


# end of file
