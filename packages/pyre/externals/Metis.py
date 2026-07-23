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


# the metis package category
class Metis(Library, family="pyre.externals.metis"):
    """
    The METIS graph partitioner
    """

    # constants
    category = "metis"

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
            headers=("metis.h",),
            # contributing this library to the link line
            libraries=("metis",),
            # and this marker to the compile line
            defines=("WITH_METIS",),
            # with database specific names where the category name isn't enough
            natives={"dpkg": ("libmetis-dev",)},
        )
        # all done
        return


# the implementation
class Default(LibraryInstallation, family="pyre.externals.metis.default", implements=Metis):
    """
    A generic METIS installation
    """

    # constants
    category = Metis.category
    flavor = category


# end of file
