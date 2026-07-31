# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .MKL import MKL


# the implementation
class Default(LibraryInstallation, family="pyre.externals.mkl.default", implements=MKL):
    """
    A generic MKL installation
    """

    # constants
    category = MKL.category
    flavor = category


# end of file
