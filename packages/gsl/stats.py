# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved
"""
Support for the gsl_stats interface
"""

# externals
from . import libgsl as gsl


# the interface for doubles
def correlation(x, y):
    """
    Compute the Pearson correlation coefficient between two vectors
    """
    # compute and return the result
    return gsl.stats_correlation(x, y)


def covariance(x, y):
    """
    Compute the covariance of two vectors
    """
    # compute and return the result
    return gsl.stats_covariance(x, y)


# end of file
