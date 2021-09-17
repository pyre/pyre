# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Specification import Specification


# class declaration
class Asset(Specification, family="merlin.projects.assets"):
    """
    Base protocol for all project assets
    """


    # required configurable state
    category = merlin.properties.str()
    category.doc = "a clue about the type of this asset"

    ignore = merlin.properties.bool(default=False)
    ignore.doc = "controls whether to ignore this asset"

    private = merlin.properties.bool(default=False)
    private.doc = "mark this asset as private"


# end of file
