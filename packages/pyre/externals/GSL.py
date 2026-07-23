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


# the gsl package category
class GSL(Library, family="pyre.externals.gsl"):
    """
    The GNU scientific library
    """

    # constants
    category = "gsl"

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
            # provable by the version header
            headers=("gsl/gsl_version.h",),
            # contributing these libraries to the link line
            libraries=("gsl", "gslcblas"),
            # and these markers to the compile line
            defines=("WITH_GSL", "HAVE_INLINE"),
            # with database specific names where the category name isn't enough
            natives={"dpkg": ("libgsl-dev", "libgsl0-dev")},
        )
        # all done
        return


# the implementation
class Default(LibraryInstallation, family="pyre.externals.gsl.default", implements=GSL):
    """
    A generic GSL installation
    """

    # constants
    category = GSL.category
    flavor = category


# end of file
