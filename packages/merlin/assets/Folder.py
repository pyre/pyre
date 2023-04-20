# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# superclass
from .RealAsset import RealAsset

# my asset category
from .Directory import Directory


# class declaration
class Folder(
    RealAsset,
    family="merlin.assets.folders.folder",
    implements=merlin.protocols.assets.folder,
):
    """
    Encapsulation of an asset container
    """

    # required configurable state
    category = merlin.protocols.assets.category()
    category.default = Directory
    category.doc = "a clue about the type of this asset"

    # interface
    def add(self, asset):
        """
        Add {asset} to my contents
        """
        # add {asset} to my pile
        self.assets.add(asset)
        # if i'm marked as ignorable
        if self.ignore:
            # mark the asset as well
            asset.ignore = True
        # all done
        return

    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my assets
        self.assets = set()
        # all done
        return

    # hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a folder
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.folder
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(folder=self, **kwds)

    # flow hooks
    def pyre_done(self, **kwds):
        """
        Hook invoked right after my factories finished refreshing me
        """
        # the trivial implementation here is just a place for a breakpoint while debugging
        # it will be removed at some point...
        # chain up
        return super().pyre_done(**kwds)


# end of file
