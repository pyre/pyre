# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .ParMetis import ParMetis


# the implementation
class Default(LibraryInstallation, family="pyre.externals.parmetis.default", implements=ParMetis):
    """
    A generic ParMETIS installation
    """

    # constants
    category = ParMetis.category
    flavor = category


# end of file
