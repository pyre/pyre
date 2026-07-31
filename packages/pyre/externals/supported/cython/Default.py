# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from ...ToolInstallation import ToolInstallation

# the protocol
from .Cython import Cython


# the implementation
class Default(ToolInstallation, family="pyre.externals.cython.default", implements=Cython):
    """
    A generic cython installation
    """

    # constants
    category = Cython.category
    flavor = category

    # user configurable state
    compiler = pyre.properties.str(default="cython")
    compiler.doc = "the name of the cython compiler"


# end of file
