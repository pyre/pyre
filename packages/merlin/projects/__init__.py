# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# implementations of the high level artifact containers
@merlin.foundry(implements=merlin.protocols.library,
                tip="a container of binary artifacts")
def library():
    """
    A container of binary artifacts
    """
    # get the project
    from .Library import Library
    # and publish it
    return Library


@merlin.foundry(implements=merlin.protocols.project,
                tip="the top level container of project artifacts")
def project():
    """
    The top level container of project artifacts
    """
    # get the project
    from .Project import Project
    # and publish it
    return Project


# end of file
