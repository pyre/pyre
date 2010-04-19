# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref
import collections


class Registrar(object):
    """
    The manager of component classes and their instances

    All Component subclasses and their instances are registered here as they encountered by the
    framework.
    """


    # public data
    extent = None # a map of component classes to their instances
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
        self.instances[cls] = weakref.WeakSet()
        # register the interface implementations
        # initialize component traits
        # all done
        return cls


    def registerComponentInstance(self, component):
        """
        """


    def registerInterfaceClass(self, interface):
        """
        """


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # the component registries
        self.instances = {}
        self.implementors = collections.defaultdict(set)
        return


# end of file 
