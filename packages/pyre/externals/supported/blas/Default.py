# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .BLAS import BLAS


# the base implementation
class Default(LibraryInstallation, family="pyre.externals.blas.default", implements=BLAS):
    """
    A generic BLAS installation
    """

    # constants
    category = BLAS.category
    flavor = category


# end of file
