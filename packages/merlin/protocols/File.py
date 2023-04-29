# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset
# schema
from .AssetCategory import AssetCategory
from .Language import Language


# class declaration
class File(Asset, family="merlin.assets.files"):
    """
    Base protocol for all file based project assets
    """


    # required configurable state
    category = AssetCategory()
    category.doc = "a clue about the type of this asset"

    language = Language()
    language.doc = "a clue about the toolchain that processes this asset"


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # publish the default implementation
        return merlin.assets.file


# end of file
