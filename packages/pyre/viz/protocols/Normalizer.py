# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the specifications of my slots
from .Real import Real
from .Unit import Unit


# the protocol of the factories that map a range of values onto [0,1]
class Normalizer(pyre.flow.producer, family="pyre.viz.normalizers"):
    """
    The normalizer protocol: map the values of a signal onto [0,1], the way the colormaps
    expect them
    """

    # the input
    signal = Real.input()
    signal.doc = "the values to normalize"

    # the output
    normalized = Unit.output()
    normalized.doc = "the values mapped onto [0,1]"

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default normalizer
        """
        # map an interval onto [0,1]
        from ..normalizers.Parametric import Parametric

        # and return it
        return Parametric


# end of file
