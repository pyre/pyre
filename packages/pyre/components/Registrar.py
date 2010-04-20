# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref
import collections
from ..patterns.Singleton import Singleton


class Registrar(object, metaclass=Singleton):
    """
    The manager of interfaces, component classes and their instances

    All Component subclasses and their instances are registered here as they encountered by the
    framework. Interfaces are registered if they are non-trivial, i.e. if their name is not
    'Interface' or '_pyre_Interface', to avoid registering the base class and the
    auto-generated interfaces from component implementation specifications.
    """


    # public data
    components = None # a map of component classes to their instances
    interfaces = None # the set of all registered interfaces
    implementors = None # a map of interfaces to components that implement them


    # interface
    def registerComponentClass(self, component):
        """
        Register the {component} class record

        The component class is added to the set of compatible implementations of all its known
        interfaces. This enables the framework to answer questions about the possible
        implementations of a given interface.
        """
        # prime the component extent
        self.components[cls] = weakref.WeakSet()
        # register the interface implementations
        # initialize component traits
        # all done
        return cls


    def registerComponentInstance(self, component):
        """
        """


    def registerInterfaceClass(self, interface):
        """
        Register {interface}
        """
        # avoid registering the base Interface class and the automatically generated
        # implementation specifications for components
        if interface._pyre_name in ["Interface", "_pyre_Interface"]:
            return interface
        # this should be a good one, so register it
        self.interfaces.add(interface)
        # and hand it back to the caller
        return interface


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # the component registries
        self.components = {}
        self.interfaces = set()
        self.implementors = collections.defaultdict(set)
        return


# end of file 
