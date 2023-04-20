# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import merlin


# the project builder
class Project(
    Fragment,
    family="merlin.builders.make.project",
    implements=merlin.protocols.flow.project,
):
    """
    Workflow generator for building projects
    """


# end of file
