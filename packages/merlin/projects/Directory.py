# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset


# class declaration
class Directory(Asset,
                family="merlin.projects.directories.directory",
                implements=merlin.protocols.directory):
    """
    Encapsulation of an asset container
    """


    # required configurable state
    category = merlin.properties.str(default="directory")
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


# end of file
