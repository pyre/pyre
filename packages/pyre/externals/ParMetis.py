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


# the parmetis package category
class ParMetis(Library, family="pyre.externals.parmetis"):
    """
    The parallel METIS graph partitioner
    """

    # constants
    category = "parmetis"

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
            headers=("parmetis.h",),
            # contributing this library to the link line
            libraries=("parmetis",),
            # and this marker to the compile line
            defines=("WITH_PARMETIS",),
            # inducing its serial partner and the message passing layer
            dependencies=("metis", "mpi"),
            # with database specific names where the category name isn't enough
            natives={"dpkg": ("libparmetis-dev",)},
        )
        # all done
        return


# the implementation
class Default(LibraryInstallation, family="pyre.externals.parmetis.default", implements=ParMetis):
    """
    A generic ParMETIS installation
    """

    # constants
    category = ParMetis.category
    flavor = category


# end of file
