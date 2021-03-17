# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
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


# end of file
