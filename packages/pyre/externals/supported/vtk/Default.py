# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .VTK import VTK


# the implementation
class Default(LibraryInstallation, family="pyre.externals.vtk.default", implements=VTK):
    """
    A generic VTK installation
    """

    # constants
    category = VTK.category
    flavor = category


# end of file
