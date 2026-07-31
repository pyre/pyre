# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base implementation
from .Default import Default


# the python 3 flavor
class Python3(Default, family="pyre.externals.python.python3"):
    """
    A python 3 installation
    """

    # constants
    flavor = "python3"


# end of file
