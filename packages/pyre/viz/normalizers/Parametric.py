# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Normalizer import Normalizer

# the specifications of my slots
from ..protocols.Real import Real
from ..protocols.Unit import Unit


# the normalizer that maps an interval onto [0,1]
class Parametric(
    pyre.flow.factory, family="pyre.viz.normalizers.parametric", implements=Normalizer
):
    """
    The filter that maps the values of a signal in its {interval} onto [0,1], the way the
    colormaps expect them
    """

    # user configurable state
    interval = pyre.properties.tuple(schema=pyre.properties.float(), default=(0, 1))
    interval.doc = "the range of values that maps onto [0,1]"

    # the input
    signal = Real.input()
    signal.doc = "the input signal"

    # the output
    normalized = Unit.output()
    normalized.doc = "the signal with its {interval} mapped onto [0,1]"


# end of file
