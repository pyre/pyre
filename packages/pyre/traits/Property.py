# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import schemata
# superclass
from .Trait import Trait


@schemata.typed
class Property(Trait.variable):
    """
    The base class for attribute descriptors that describe a component's external state
    """


    # framework data
    isConfigurable = True # slotted traits are configurable


    # mixins to be included to my type offering
    class decimal:
        """Mixin for handling decimal values"""

        # override the default node builder
        def buildSlot(self, model, **kwds):
            # decimals prefer expressions
            return model.expression(postprocessor=self, **kwds)

    class dimensional:
        """Mixin for handling quantities with units"""

        # override the default node builder
        def buildSlot(self, model, **kwds):
            # dimensionals prefer expressions
            return model.expression(postprocessor=self, **kwds)

    class float:
        """Mixin for handling floating point values"""

        # override the default node builder
        def buildSlot(self, model, **kwds):
            # floats prefer expressions
            return model.expression(postprocessor=self, **kwds)

    class int:
        """Mixin for handling integer values"""

        # override the default node builder
        def buildSlot(self, model, **kwds):
            # integers prefer expressions
            return model.expression(postprocessor=self, **kwds)


    # framework support
    def buildSlot(self, model, **kwds):
        """
        The default node building strategy
        """
        # build an interpolation with me as its value postprocessor
        return model.interpolation(postprocessor=self.coerce, **kwds)


    # meta-methods
    def __get__(self, instance, cls):
        """
        Retrieve the value of this trait
        """
        # find out whose inventory we are supposed to access
        configurable = instance if instance else cls
        # grab the slot from the client's inventory
        slot = configurable.pyre_inventory[self]
        # compute and return its value
        return slot.value


    def __str__(self):
        return "{0.name!r}: a property of type {0.typename!r}".format(self)


# end of file 
