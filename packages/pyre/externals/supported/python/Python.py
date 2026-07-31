# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from ...Library import Library
from ...Tool import Tool

# the flavor description
from ...Recipe import Recipe


# the python package category
class Python(Tool, Library, family="pyre.externals.python"):
    """
    The python interpreter and its development artifacts
    """

    # constants
    category = "python"

    # user configurable state
    interpreter = pyre.properties.str(default="python3")
    interpreter.doc = "the name of the python interpreter"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors
        """
        # get the implementations
        from .Python3 import Python3

        # python 3
        yield Recipe(
            # of this category
            category=cls.category,
            # the flavor tag
            flavor="python3",
            # realized by the python 3 installation
            factory=Python3,
            # a selection group on package managers with alternatives
            group="python3",
            # provable by the development header
            headers=("Python.h",),
            # the library stem carries the version and the ABI tags; resolve the actual one
            libraries=(r"python3\.\d+[tdm]*",),
            # the interpreter executable, possibly decorated with version and ABI tags
            binaries={"interpreter": r"python3(\.\d+)?[tdm]*"},
            # the marker for the compile line
            defines=("WITH_PYTHON", "WITH_PYTHON3"),
            # with database specific names where the flavor name isn't enough; on dpkg, the
            # {-dev} names are metapackages, so the versioned {libpython3.x-dev} carries the
            # actual files and is reachable by prefix matching, while the interpreter itself
            # lives in the versioned {python3.x-minimal} companions
            natives={
                "conda": ("python",),
                "dpkg": (("libpython3", "python3."), ("python3-dev", "python3.")),
                "rpm": (("python3-devel", "python3"),),
            },
        )
        # all done
        return


# end of file
