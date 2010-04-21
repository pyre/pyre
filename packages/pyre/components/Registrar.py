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
        # avoid registering the base Component class
        if component._pyre_name is "Component":
            return component
        # prime the component extent
        self.components[component] = weakref.WeakSet()
        # register the interface implementations
        self._recordInterfaceImplementations(component)
        # all done
        return component


    def registerComponentInstance(self, component):
        """
        Register the {component} instance
        """
        # add {component} to the set of registered instances of its class
        # Actor, the Component metaclass, guarantees that component classes get registered
        # before any of their instances, so the look up for the class should never fail
        self.components[component.__class__].add(component)
        # and hand it back
        return component


    def registerInterfaceClass(self, interface):
        """
        Register {interface}
        """
        # avoid registering the base Interface class and the automatically generated
        # implementation specifications for components
        if interface._pyre_name in self._IGNORABLES:
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


    # implementation details
    def _recordInterfaceImplementations(self, component):
        """
        Add the {component} class record to the set of implementors of all its interfaces
        """
        # access the interface implementation specification
        implements = component._pyre_implements
        # bail out if no specification was provided by the author of the component
        if not implements:
            return component
        # get access to the interface metaclass
        from .Role import Role
        # otherwise, look through its
        for interface in implements.__mro__:
            # ignore the trivial interfaces
            if not isinstance(interface, Role) or interface._pyre_name in self._IGNORABLES:
                continue
            # otherwise, update the set of implementors of this interface
            self.implementors[interface].add(component)
        # all done
        return


    # constants
    _IGNORABLES = {"_pyre_Interface", "Interface"}


# end of file 
