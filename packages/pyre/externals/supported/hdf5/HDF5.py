# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...Library import Library

# the flavor description
from ...Recipe import Recipe


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
        # get the implementations
        from .Default import Default

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
            natives={
                "dpkg": ("libhdf5-dev",),
                "rpm": ("hdf5-devel", "hdf5-openmpi-devel", "hdf5-mpich-devel"),
            },
        )
        # all done
        return


# end of file
