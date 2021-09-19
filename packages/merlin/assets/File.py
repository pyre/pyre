# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .RealAsset import RealAsset


# class declaration
class File(RealAsset,
           family="merlin.assets.files.file",
           implements=merlin.protocols.file):
    """
    Encapsulation of a file based project asset
    """


    # required configurable state
    category = merlin.properties.str()
    category.doc = "a clue about the type of this asset"

    language = merlin.protocols.language()
    language.doc = "a clue about the toolchain that processes this asset"


    # hooks
    def identify(self, authority, **kwds):
        """
        Ask {authority} to process a file based asset
        """
        # attempt to
        try:
            # ask authority for a handler for my type
            handler = authority.file
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(authority=authority)
        # if it does, invoke it
        return handler(file=self, **kwds)


# end of file
