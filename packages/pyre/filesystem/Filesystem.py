# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Folder import Folder
from . import _metaclass_Filesystem


class Filesystem(Folder, metaclas=_metaclass_Filesystem):
    """
    The base class for representing filesystems
    """


    def __init__(self, **kwds):
        super().__init__(**kwds)
        return


# end of file 
