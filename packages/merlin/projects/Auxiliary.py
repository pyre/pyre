# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Auxiliary(merlin.component,
                family="merlin.assets.categories.auxiliary",
                implements=merlin.protocols.assetCategory):
    """
    The category of auxiliary assets
    """


    # constants
    category = "auxiliary"


# end of file
