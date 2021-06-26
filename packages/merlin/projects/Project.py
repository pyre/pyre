# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Project(merlin.component,
              family="merlin.projects.project", implements=merlin.protocols.project):
    """
    A high level container of artifacts
    """


    # required state
    libraries = merlin.properties.tuple(schema=merlin.protocols.library())
    libraries.doc = "the collection of project libraries"


# end of file
