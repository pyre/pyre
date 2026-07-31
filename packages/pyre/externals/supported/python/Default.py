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
from .Python import Python


# the base implementation
class Default(
    ToolInstallation,
    LibraryInstallation,
    family="pyre.externals.python.default",
    implements=Python,
):
    """
    A generic python installation
    """

    # constants
    category = Python.category
    flavor = category

    # user configurable state
    interpreter = pyre.properties.str(default="python3")
    interpreter.doc = "the name of the python interpreter"


# end of file
