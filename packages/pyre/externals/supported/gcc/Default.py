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
from .GCC import GCC


# the implementation
class Default(ToolInstallation, family="pyre.externals.gcc.default", implements=GCC):
    """
    A generic GCC installation
    """

    # constants
    category = GCC.category
    flavor = category

    # user configurable state
    wrapper = pyre.properties.str(default="gcc")
    wrapper.doc = "the name of the compiler front end"


# end of file
