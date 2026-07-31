# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .Eigen import Eigen


# the implementation
class Default(LibraryInstallation, family="pyre.externals.eigen.default", implements=Eigen):
    """
    A generic Eigen installation
    """

    # constants
    category = Eigen.category
    flavor = category


# end of file
