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


# the cython package category
class Cython(Tool, family="pyre.externals.cython"):
    """
    The cython compiler
    """

    # constants
    category = "cython"

    # user configurable state
    compiler = pyre.properties.str(default="cython")
    compiler.doc = "the name of the cython compiler"

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
            group="cython",
            # the compiler executable
            binaries={"compiler": "cython"},
            # with database specific names where the category name isn't enough; macports
            # buries the version tag in the middle of the name, hence the pattern
            natives={
                "dpkg": ("cython3", "cython"),
                "macports": (r"py3\d+-cython",),
            },
        )
        # all done
        return


# end of file
