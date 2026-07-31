# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...Library import Library

# the flavor description
from ...Recipe import Recipe


# the vtk package category
class VTK(Library, family="pyre.externals.vtk"):
    """
    The visualization toolkit
    """

    # constants
    category = "vtk"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors
        """
        # get the implementations
        from .Default import Default

        # there is only one flavor
        yield Recipe(
            # of this category
            category=cls.category,
            # realized by the generic installation
            factory=Default,
            # provable by the version header, wherever the versioned include directory is
            headers=("vtkVersion.h",),
            # the core library stem carries the version; resolve the actual one
            libraries=(r"vtkCommonCore(-\d+\.\d+)?",),
            # the marker for the compile line
            defines=("WITH_VTK",),
            # with database specific names where the category name isn't enough
            natives={"dpkg": ("libvtk9-dev", "libvtk7-dev")},
        )
        # all done
        return


# end of file
