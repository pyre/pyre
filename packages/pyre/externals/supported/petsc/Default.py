# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .PETSc import PETSc


# the implementation
class Default(LibraryInstallation, family="pyre.externals.petsc.default", implements=PETSc):
    """
    A generic PETSc installation
    """

    # constants
    category = PETSc.category
    flavor = category


# end of file
