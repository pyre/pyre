# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# superclass
from .InfoZip import InfoZip
from .InfoDirectory import InfoDirectory


# class declaration
class InfoZipDirectory(InfoZip, InfoDirectory):
    """
    Representation of zip filesystem directories
    """


# end of file
