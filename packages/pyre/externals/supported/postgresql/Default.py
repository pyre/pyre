# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from ...LibraryInstallation import LibraryInstallation
from ...ToolInstallation import ToolInstallation

# the protocol
from .Postgres import Postgres


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
