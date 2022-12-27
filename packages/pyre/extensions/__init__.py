# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


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


# end of file
