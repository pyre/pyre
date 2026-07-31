# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .FFTW import FFTW


# the implementation
class Default(LibraryInstallation, family="pyre.externals.fftw.default", implements=FFTW):
    """
    A generic FFTW installation
    """

    # constants
    category = FFTW.category
    flavor = category


# end of file
