# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Executive import Executive
from ..patterns.Singleton import Singleton


class Pyre(Executive, metaclass=Singleton):

    """
    The framework executive singleton
    """


# end of file 
