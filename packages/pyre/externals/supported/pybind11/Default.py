# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .Pybind11 import Pybind11


# the implementation
class Default(LibraryInstallation, family="pyre.externals.pybind11.default", implements=Pybind11):
    """
    A generic pybind11 installation
    """

    # constants
    category = Pybind11.category
    flavor = category


# end of file
