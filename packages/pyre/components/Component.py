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


    # meta methods
    def __init__(self, name, **kwds):
        super().__init__(**kwds)

        # store my name
        self._pyre_name = name
        # build my inventory instance by calling the constructor that my metaclass attached at
        # compile time
        self._pyre_inventory = self._pyre_Inventory()
        # register me with the component registrar


# end of file 
