# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .RealAsset import RealAsset


# class declaration
class File(RealAsset, family="merlin.assets.files.file", implements=merlin.protocols.file):
    """
    Encapsulation of a file based project asset
    """


    # required configurable state
    category = merlin.protocols.assetCategory()
    category.doc = "a clue about the type of this asset"

    language = merlin.protocols.language()
    language.doc = "a clue about the toolchain that processes this asset"


    # hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a file based asset
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.file
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(file=self, **kwds)


# end of file
