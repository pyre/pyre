# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset
# schema
from .Language import Language


# class declaration
class File(Asset, family="merlin.projects.files"):
    """
    Base protocol for all file based project assets
    """


    # required configurable state
    category = merlin.properties.str()
    category.doc = "a clue about the type of this asset"

    language = Language()
    language.doc = "a clue about the toolchain that processes this asset"


# end of file
