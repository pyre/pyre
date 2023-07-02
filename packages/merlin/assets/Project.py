# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# superclass
from .Asset import Asset


# class declaration
class Project(
    Asset, family="merlin.assets.project", implements=merlin.protocols.assets.project
):
    """
    A high level container of assets
    """

    # required state
    libraries = merlin.properties.tuple(schema=merlin.protocols.assets.library())
    libraries.doc = "the collection of project libraries"

    # hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a project
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.project
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(project=self, **kwds)


# end of file
