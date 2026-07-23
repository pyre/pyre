# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from .Tool import Tool
from .ToolInstallation import ToolInstallation

# the flavor description
from .Recipe import Recipe


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
            # with database specific names where the category name isn't enough
            natives={"dpkg": ("cython3", "cython")},
        )
        # all done
        return


# the implementation
class Default(ToolInstallation, family="pyre.externals.cython.default", implements=Cython):
    """
    A generic cython installation
    """

    # constants
    category = Cython.category
    flavor = category

    # user configurable state
    compiler = pyre.properties.str(default="cython")
    compiler.doc = "the name of the cython compiler"


# end of file
