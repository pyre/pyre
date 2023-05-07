# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# superclass
from .Asset import Asset

# schema
from ..languages.Table import Table as table


# class declaration
class Library(Asset, family="merlin.assets.libraries"):
    """
    A high level container of binary artifacts
    """

    # user configurable state
    name = merlin.properties.str()
    name.doc = "the name of the library; used as a seed to name its various assets"

    root = merlin.properties.path()
    root.doc = "the path to the library source relative to the root of the repository"

    languages = table()
    languages.doc = "language specific configuration"

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # grab the library foundry and return it
        return merlin.assets.library


# end of file
