# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .NumPy import NumPy


# the implementation
class Default(LibraryInstallation, family="pyre.externals.numpy.default", implements=NumPy):
    """
    A generic numpy installation
    """

    # constants
    category = NumPy.category
    flavor = category


# end of file
