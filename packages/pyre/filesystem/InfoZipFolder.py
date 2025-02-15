# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# superclass
from .InfoZip import InfoZip
from .InfoFolder import InfoFolder


# class declaration
class InfoZipFolder(InfoZip, InfoFolder):
    """
    Representation of zip filesystem directories
    """


# end of file
