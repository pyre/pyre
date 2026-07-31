# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...LibraryInstallation import LibraryInstallation

# the protocol
from .HDF5 import HDF5


# the implementation
class Default(LibraryInstallation, family="pyre.externals.hdf5.default", implements=HDF5):
    """
    A generic serial HDF5 installation
    """

    # constants
    category = HDF5.category
    flavor = category
    tags = ("serial",)


# end of file
