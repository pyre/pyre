# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Product import Product


# class declaration
class Asset(Product):
    """
    Encapsulation of a project asset
    """


    # required configurable state
    category = merlin.properties.str()
    category.doc = "a clue about the type of this asset"

    ignore = merlin.properties.bool(default=False)
    ignore.doc = "controls whether to ignore this asset"

    private = merlin.properties.bool(default=False)
    private.doc = "mark this asset as private"


# end of file
