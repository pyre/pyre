# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset


# class declaration
class File(Asset, family="merlin.projects.files"):
    """
    Base protocol for all project assets
    """


    # required configurable state
    language = merlin.properties.str()
    language.doc = "a clue about the toolchain that processes this asset"


# end of file
