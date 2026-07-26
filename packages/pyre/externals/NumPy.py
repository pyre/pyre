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


# the numpy package category
class NumPy(Library, family="pyre.externals.numpy"):
    """
    The numpy array package and its C API

    The headers live wherever the interpreter's site packages are; the discovery is driven
    entirely by the package contents, so no knowledge of the site layout is required
    """

    # constants
    category = "numpy"

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
            # provable by the C API header, wherever the site packages put it
            headers=("numpy/arrayobject.h",),
            # the C API is consumed through the headers; no libraries on the link line
            libraries=(),
            # the marker for the compile line
            defines=("WITH_NUMPY",),
            # with database specific names where the category name isn't enough; macports
            # buries the version tag in the middle of the name, hence the pattern
            natives={
                "dpkg": ("python3-numpy",),
                "macports": (r"py3\d+-numpy",),
                "rpm": ("python3-numpy",),
            },
            # and a dependency on python
            dependencies=("python",),
        )
        # all done
        return


# the implementation
class Default(LibraryInstallation, family="pyre.externals.numpy.default", implements=NumPy):
    """
    A generic numpy installation
    """

    # constants
    category = NumPy.category
    flavor = category


# end of file
