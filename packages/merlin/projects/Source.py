# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Source(merlin.component,
             family="merlin.assets.categories.source",
             implements=merlin.protocols.assetCategory):
    """
    Encapsulation of a source file
    """


    # constants
    category = "source"


# end of file
