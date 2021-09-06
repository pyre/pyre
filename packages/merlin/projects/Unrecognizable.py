# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Unrecognizable(merlin.component,
                     family="merlin.projects.categories.unrecognizable",
                     implements=merlin.protocols.assetCategory):
    """
    Encapsulation of a file whose purpose is not known
    """


    # constants
    category = "unrecognizable"


# end of file
