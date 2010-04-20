# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Role import Role
from .Configurable import Configurable


class Interface(Configurable, metaclass=Role):
    """
    The base class for requirement specifications
    """


    # framework data
    _pyre_name = None # my name; for interfaces, this derived form the class __name__
    _pyre_configurables = None # a tuple of all my ancestors that derive from Configurable
    _pyre_traits = None # a list of all the traits in my declaration


# end of file 
