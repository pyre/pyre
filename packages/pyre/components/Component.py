# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Actor import Actor
from .Configurable import Configurable


class Component(Configurable, metaclass=Actor):
    """
    The base class for all components
    """


    # framework data
    _pyre_name = None # my public name
    _pyre_family = None # my public name
    _pyre_implements = None # the list of interfaces implemented by this component
    _pyre_configurables = None # a tuple of all my ancestors that derive from Configurable

    _pyre_traits = None # a list of the traits found in my declaration
    _pyre_inventory = None # per-instance storage for trait values; built by Actor


    # class interface
    @classmethod
    def pyre_getPackageName(cls):
        """
        Extract the name of the package that this component is a part of by splitting the
        family name apart based on the _pyre_FAMILY_SEPARATOR and returning the leading
        fragment
        """
        # bail out if there is not family name
        if not cls._pyre_family: return None
        # otherwise, split the family name na dreturn the first fragment
        return cls._pyre_family.split(cls._pyre_FAMILY_SEPARATOR)[0]


    # meta methods
    def __init__(self, name, **kwds):
        super().__init__(**kwds)

        # store my name
        self._pyre_name = name
        # build my inventory instance by calling the constructor that my metaclass attached at
        # compile time
        self._pyre_inventory = self._pyre_Inventory()
        # register me with the component registrar


    # constants
    _pyre_FAMILY_SEPARATOR = '.'


# end of file 
