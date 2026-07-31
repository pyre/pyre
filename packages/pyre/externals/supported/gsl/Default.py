# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .GSL import GSL


# the implementation
class Default(LibraryInstallation, family="pyre.externals.gsl.default", implements=GSL):
    """
    A generic GSL installation
    """

    # constants
    category = GSL.category
    flavor = category


# end of file
