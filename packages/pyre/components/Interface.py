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


    # interface
    @classmethod
    def pyre_cast(cls, configurable, name, value):
        """
        Convert {specification} into an actual component instance that is type compatible with me
        """
        # if value is a string
        if isinstance(value, str):
            # get the pyre executive to convert it to a component factory
            factory = cls._pyre_executive.retrieveComponentDescriptor(value)
            
        # build the name of the instance
        tag = cls._pyre_FAMILY_SEPARATOR.join(filter(None, [configurable._pyre_name, name]))
        # attempt to instantiate it
        return factory(name=tag)


# end of file 
