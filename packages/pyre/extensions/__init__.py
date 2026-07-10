# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Package that serves as a resting place of the various extension modules
"""

# attempt to
try:
    # get the pyre bindings
    from . import pyre as libpyre
# if something goes wrong
except ImportError:
    # mark; the rest of the package will adjust
    libpyre = None


# attempt to
try:
    # load the {hdf5} bindings
    from . import h5 as libh5
# if anything goes wrong
except ImportError:
    # just mark it as unavailable
    libh5 = None
# otherwise
else:
    # initialize the {hdf5} runtime
    libh5.init()


# attempt to
try:
    # load the {postgres} bindings
    from . import postgres as libpq
# if they were never built, this build has no postgres support; note that the exception must be
# this narrow: bindings that exist but refuse to load are a bug, and a bug that presents itself
# as the tranquil absence of a library is one that nobody ever finds
except ModuleNotFoundError:
    # just mark it as unavailable
    libpq = None


# end of file
