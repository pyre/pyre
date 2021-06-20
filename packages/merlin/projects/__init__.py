# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# implementations of the high level asset containers
@merlin.foundry()
def library(implements=merlin.protocols.library, tip="a container of binary assets"):
    """
    A container of binary assets
    """
    # get the project
    from .Library import Library
    # and publish it
    return Library


@merlin.foundry()
def project(implements=merlin.protocols.project, tip="the top level container of project assets"):
    """
    The top level container of project assets
    """
    # get the project
    from .Project import Project
    # and publish it
    return Project


# end of file
