# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Template(merlin.component,
               family="merlin.assets.categories.template",
               implements=merlin.protocols.assetCategory):
    """
    Encapsulation of a template file that generates other sources
    """


    # constants
    category = "template"


# end of file
