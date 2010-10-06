# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Role import Role
from .Actor import Actor
from .Configurable import Configurable


class Interface(Configurable, metaclass=Role, hidden=True):
    """
    The base class for requirement specifications
    """


    # framework data; inherited from Configurable and repeated here for clarity
    pyre_name = None # the instance name
    pyre_state = None # track progress through the bootsrapping process
    pyre_namemap = None # a map of descriptor aliases to their canonical names
    pyre_localTraits = None # a tuple of all the traits in my declaration
    pyre_inheritedTraits = None # a tuple of all the traits inheited from my superclasses
    pyre_pedigree = None # a tuple of ancestors that are themselves configurables


    # interface
    @classmethod
    def pyre_cast(cls, value):
        """
        Convert {value} into a component factory that is assignment compatible with me
        """
        raise NotImplementedError("NYI!")


    # exceptions
    from .exceptions  import InterfaceError
    from ..schema.exceptions import CastingError


# end of file 
