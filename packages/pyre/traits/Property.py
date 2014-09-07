# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import collections # for sequence checking
from .. import schemata # type information
# superclass
from .Slotted import Slotted


# declaration
@schemata.typed
class Property(Slotted):
    """
    The base class for traits that correspond to simple types
    """


    # mixins to be included to my type offering
    class schema:
        """Mixin for handling decimal values"""

        # override the default expression handler
        @property
        def macro(self):
            """
            Access to the default strategy for handling macros in slot values
            """
            # by default, build interpolations
            return self.pyre_nameserver.interpolation


    class numeric:
        """Mixin for handling numeric types"""

        # override the default expression handler
        @property
        def macro(self):
            """
            Access to the default strategy for handling macros for numeric types
            """
            # build expressions
            return self.pyre_nameserver.expression


    class sequences:
        """Mixin for handling typed containers"""

        # override the default expression handler
        def macro(self, value, **kwds):
            """
            Access to the default strategy for handling macros in sequences
            """
            # if the value is a string
            if isinstance(value, str):
                # do whatever my schema specifies
                return self.schema.macro(value=value, **kwds)

            # if the value is a sequence
            if isinstance(value, collections.Iterable):
                # convert the items into nodes
                nodes = (self.schema.macro(item) for item in value)
                # and attach them to a sequence node
                return self.pyre_nameserver.sequence(nodes=nodes, **kwds)

            # if the value is already some kind of node
            if isinstance(value, self.pyre_nameserver.node):
                # just return it
                return value

            # shouldn't get here
            assert False, 'unreachable'


    # meta-methods
    def __init__(self, classSlot=None, instanceSlot=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # build my slot factories
        self.classSlot = classSlot or self.factory(trait=self, processor=self.process)
        self.instanceSlot = instanceSlot or self.factory(trait=self, processor=self.process)
        # all done
        return


    def __str__(self):
        return "{0.name!r}: a property of type {0.typename!r}".format(self)


# end of file 
