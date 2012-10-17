# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# metaclass
from .Role import Role
# superclass
from .Configurable import Configurable


# class declaration
class Protocol(Configurable, metaclass=Role, internal=True):
    """
    The base class for requirement specifications
    """


    @classmethod
    def pyre_default(cls):
        """
        The preferred implementation of this protocol, in case the user has not provided an
        alternative
        """
        # actual protocols should override
        return None


# end of file 
