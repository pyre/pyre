# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from ...Tool import Tool

# the flavor description
from ...Recipe import Recipe


# the gcc package category
class GCC(Tool, family="pyre.externals.gcc"):
    """
    The GNU compiler collection
    """

    # constants
    category = "gcc"

    # user configurable state
    wrapper = pyre.properties.str(default="gcc")
    wrapper.doc = "the name of the compiler front end"

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
            # a selection group on package managers with alternatives
            group="gcc",
            # the front end, possibly decorated with a version tag
            binaries={"wrapper": r"gcc(-mp-\d+|-\d+)?"},
            # with database specific names where the category name isn't enough
            natives={"macports": ("mp-gcc", "gcc")},
        )
        # all done
        return


# end of file
