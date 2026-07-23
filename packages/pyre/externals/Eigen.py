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


# the eigen package category
class Eigen(Library, family="pyre.externals.eigen"):
    """
    The Eigen template library for linear algebra

    Eigen is header only; the recipe expects no libraries, which makes it a good example of
    how far the declarative description reaches
    """

    # constants
    category = "eigen"

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
            # provable by the core header; the include directory is discovered wherever the
            # package database put it, e.g. {include/eigen3} on macports and dpkg
            headers=("Eigen/Core",),
            # header only: no libraries
            libraries=(),
            # the marker for the compile line
            defines=("WITH_EIGEN",),
            # with database specific names where the category name isn't enough
            natives={
                "dpkg": ("libeigen3-dev",),
                "macports": ("eigen3",),
            },
        )
        # all done
        return


# the implementation
class Default(LibraryInstallation, family="pyre.externals.eigen.default", implements=Eigen):
    """
    A generic Eigen installation
    """

    # constants
    category = Eigen.category
    flavor = category


# end of file
