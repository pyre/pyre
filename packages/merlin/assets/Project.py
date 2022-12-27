# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset


# class declaration
class Project(Asset,
              family="merlin.assets.project", implements=merlin.protocols.project):
    """
    A high level container of assets
    """


    # required state
    libraries = merlin.properties.tuple(schema=merlin.protocols.library())
    libraries.doc = "the collection of project libraries"


# end of file
