# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from .Library import Library
from .LibraryInstallation import LibraryInstallation
from .Tool import Tool
from .ToolInstallation import ToolInstallation

# the flavor description
from .Recipe import Recipe


# the postgres package category
class Postgres(Tool, Library, family="pyre.externals.postgres"):
    """
    The client artifacts of the postgres database server
    """

    # constants
    category = "postgresql"

    # user configurable state
    psql = pyre.properties.str(default="psql")
    psql.doc = "the name of the postgres client"

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
            group="postgresql",
            # provable by the client library header
            headers=("libpq-fe.h",),
            # contributing this library to the link line
            libraries=("pq",),
            # the client executable
            binaries={"psql": "psql"},
            # the marker for the compile line
            defines=("WITH_PQ",),
            # with database specific names where the category name isn't enough; debian
            # splits the client into versioned {postgresql-client} packages, so they ride
            # along as companions
            natives={
                "conda": ("libpq", "postgresql"),
                "dpkg": (("libpq-dev", "postgresql-client"),),
                "rpm": (("libpq-devel", "postgresql"),),
            },
        )
        # all done
        return


# the implementation
class Default(
    ToolInstallation,
    LibraryInstallation,
    family="pyre.externals.postgres.default",
    implements=Postgres,
):
    """
    A generic postgres client installation
    """

    # constants
    category = Postgres.category
    flavor = category

    # user configurable state
    psql = pyre.properties.str(default="psql")
    psql.doc = "the name of the postgres client"


# end of file
