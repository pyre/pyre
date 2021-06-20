# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Project(merlin.component,
              family="merlin.projects.basic", implements=merlin.protocols.project):
    """
    A high level container of assets
    """


# end of file
