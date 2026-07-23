# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from .Library import Library
from .LibraryInstallation import LibraryInstallation

# the flavor description
from .Recipe import Recipe


# the hdf5 package category
class HDF5(Library, family="pyre.externals.hdf5"):
    """
    The HDF5 data model and file format
    """

    # constants
    category = "hdf5"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors
        """
        # the serial flavor
        yield Recipe(
            # of this category
            category=cls.category,
            # realized by the generic installation
            factory=Default,
            # provable by the top level header
            headers=("hdf5.h",),
            # contributing these libraries to the link line
            libraries=("hdf5_cpp", "hdf5"),
            # and this marker to the compile line
            defines=("WITH_HDF5",),
            # with database specific names where the category name isn't enough
            natives={"dpkg": ("libhdf5-dev",)},
        )
        # all done
        return


# the implementation
class Default(LibraryInstallation, family="pyre.externals.hdf5.default", implements=HDF5):
    """
    A generic HDF5 installation
    """

    # constants
    category = HDF5.category
    flavor = category


# end of file
