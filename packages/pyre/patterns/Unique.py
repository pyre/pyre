# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Type import Type


# declaration
class Unique(Type):
    """
    Support for classes with named instances that are placed in a registry upon construction

    The instance registry is created and attached to the first base class in a hierarchy that
    mentions {Unique} as its metaclass. Subclasses that want their own registry must set
    {pyre_unique} to {True} in their class declaration.

    The instance registry is expected to be a map (name -> instance), which assumes that the
    constructor takes {name} as an argument. Classes can override this behavior by overriding
    the class method {pyre_hashInstance} to generate a custom key. The signature of this method
    should be identical to the constructor's.

    Instances of {Unique} can participate in the creation of their instance index by overriding
    the class method {pyre_createRegistry}.
    """


    # metamethods
    def __init__(self, name, bases, attributes, *, pyre_unique=False, **kwds):
        """
        Endow the class record being decorated with a map
        """
        # chain up
        super().__init__(name, bases, attributes, **kwds)

        # initialize the class registry. this happens only if the user has marked this class as
        # the keeper of the registry by explicitly setting {pyre_registrar} to {True}, of if
        # the attribute that holds the registry is missing, which is true only for the first
        # class in the hierarchy that mentions {Registrar} as its metaclass
        if pyre_unique or not hasattr(self, "pyre_unique"):
            # build the registry
            self.pyre_unique = self.pyre_createRegistry()

        # all done
        return


    def __call__(self, **kwds):
        """
        Look for a registered instance and return it; if not there, create one, register it,
        and return it
        """
        # get the registry; subclasses that want a separate one from their ancestors must
        # declare one
        registry = self.pyre_unique
        # hash the instance
        key = self.pyre_hashInstance(**kwds)
        # if there is a registered instance
        if key in registry:
            # get it and return it
            return registry[key]
        # otherwise, make one
        instance = super().__call__(**kwds)
        # register it
        registry[key] = instance
        # and return it
        return instance


    # implementation details
    def pyre_createRegistry(self):
        """
        Build and initialize the instance registry
        """
        # use a simple dictionary, by default
        return {}


    def pyre_hashInstance(self, name, **kwds):
        """
        Assume that {name} is provided at construction time and use it as the instance hash
        """
        # easy enough
        return name


# end of file
