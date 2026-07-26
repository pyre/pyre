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


# the petsc package category
class PETSc(Library, family="pyre.externals.petsc"):
    """
    The portable extensible toolkit for scientific computation
    """

    # constants
    category = "petsc"

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
            # provable by the top level header
            headers=("petsc.h",),
            # contributing this library to the link line
            libraries=("petsc",),
            # and this marker to the compile line
            defines=("WITH_PETSC",),
            # inducing the message passing layer
            dependencies=("mpi",),
            # with database specific names where the category name isn't enough
            natives={
                "dpkg": ("petsc-dev", "libpetsc-real-dev"),
                "rpm": ("petsc-devel",),
            },
        )
        # all done
        return


# the implementation
class Default(LibraryInstallation, family="pyre.externals.petsc.default", implements=PETSc):
    """
    A generic PETSc installation
    """

    # constants
    category = PETSc.category
    flavor = category


# end of file
