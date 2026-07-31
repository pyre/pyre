# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .Metis import Metis


# the implementation
class Default(LibraryInstallation, family="pyre.externals.metis.default", implements=Metis):
    """
    A generic METIS installation
    """

    # constants
    category = Metis.category
    flavor = category


# end of file
