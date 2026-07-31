# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from ...LibraryInstallation import LibraryInstallation
from ...ToolInstallation import ToolInstallation

# the protocol
from .CUDA import CUDA


# the implementation
class Default(
    ToolInstallation,
    LibraryInstallation,
    family="pyre.externals.cuda.default",
    implements=CUDA,
):
    """
    A generic CUDA toolkit installation
    """

    # constants
    category = CUDA.category
    flavor = category

    # user configurable state
    compiler = pyre.properties.str(default="nvcc")
    compiler.doc = "the name of the cuda compiler driver"


# end of file
