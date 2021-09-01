# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Asset(merlin.protocol, family="merlin.projects.sources"):
    """
    Base protocol for all project assets
    """


    # required configurable state
    ignore = merlin.properties.bool(default=False)
    ignore.doc = "controls whether to ignore this asset"


# end of file
