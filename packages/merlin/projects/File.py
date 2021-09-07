# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset


# class declaration
class File(Asset,
           family="merlin.projects.files.file",
           implements=merlin.protocols.file):
    """
    Encapsulation of a file based project asset
    """


    # required configurable state
    language = merlin.protocols.language()
    language.doc = "a clue about the toolchain that processes this asset"


# end of file
