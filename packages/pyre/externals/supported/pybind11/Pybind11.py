# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...Library import Library

# the flavor description
from ...Recipe import Recipe


# the pybind11 package category
class Pybind11(Library, family="pyre.externals.pybind11"):
    """
    The pybind11 binding generator; header only
    """

    # constants
    category = "pybind11"

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
            # provable by the main header
            headers=("pybind11/pybind11.h",),
            # header only: no libraries
            libraries=(),
            # the marker for the compile line
            defines=("WITH_PYBIND11",),
            # with database specific names where the category name isn't enough
            natives={
                "dpkg": ("pybind11-dev",),
                "rpm": ("pybind11-devel",),
            },
            # and a dependency on python
            dependencies=("python",),
        )
        # all done
        return


# end of file
