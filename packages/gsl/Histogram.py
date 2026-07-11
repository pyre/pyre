# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
from . import libgsl as gsl


# the class declaration
class Histogram(gsl.Histogram):
    """
    A histogram of doubles

    The histogram itself -- its bins, its counts, its statistics, its arithmetic -- is the
    extension's. This subclass adds the two conveniences that reach for a {gsl.Vector}: filling
    from a run of samples, and handing the counts back as a vector
    """

    # types
    from .Vector import Vector as vector

    # interface
    def fill(self, values):
        """
        Increment my counts once for each sample in {values}
        """
        # for each sample
        for x in values:
            # bump the bin that holds it
            self.increment(x)
        # and return me
        return self

    def counts(self):
        """
        Return my bin counts as a vector
        """
        # make a vector of my shape
        result = self.vector(shape=self.bins)
        # fill it with my counts
        for i in range(self.bins):
            # one bin at a time
            result[i] = self[i]
        # and return it
        return result


# end of file
