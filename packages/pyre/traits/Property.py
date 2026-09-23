# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc  # for sequence checking
from .. import schemata  # type information

# superclass
from .Slotted import Slotted


# declaration
@schemata.typed
class Property(Slotted):
    """
    The base class for traits that correspond to simple types
    """

    # framework data
    category = "property"
    # predicate that indicates whether this trait is a property
    isProperty = True

    # mixins to be included to my type offering
    class schema:
        """Mixin for handling generic values"""

        # override the default expression handler
        @property
        def macro(self):
            """
            The default strategy for handling macros in slot values
            """
            # by default, build interpolations
            return self.pyre_nameserver.interpolation

        @property
        def native(self):
            """
            The strategy for building slots from more complex input values
            """
            return self.pyre_nameserver.variable

    class array:
        """Mixin for arrays, whose items are numbers"""

        # metamethods
        def __init__(self, schema=None, **kwds):
            # an unspecified schema for my items is the trait counterpart of the schemata
            # default, which is a float
            if schema is None:
                # so make one
                schema = self.float()
            # chain up
            super().__init__(schema=schema, **kwds)
            # all done
            return

    class numbers:
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

        # metamethods
        def __init__(self, schema=None, **kwds):
            # the schema of my items must come from the trait layer, since the configuration
            # store asks it for the {macro} and {native} strategies; the schemata ancestors
            # default to bare declarators that have neither, so an unspecified schema is
            # replaced by the trait counterpart of theirs: items are passed through as they are
            if schema is None:
                # so make an identity trait
                schema = self.identity()
            # chain up
            super().__init__(schema=schema, **kwds)
            # all done
            return

        # override the default expression handler
        @property
        def macro(self):
            """
            The default strategy for handling slot values that are strings and therefore
            subject to some kind of evaluation in the context of the configuration store
            """
            # whatever my schema says
            return self.schema.macro

        def native(self, value, **kwds):
            """
            The strategy for building slots from more complex input values
            """
            # if the value is a sequence
            if isinstance(value, collections.abc.Iterable):
                # convert the items into nodes
                nodes = (self.schema.macro(value=item) for item in value)
                # and attach them to a sequence node
                return self.pyre_nameserver.sequence(nodes=nodes, **kwds)

            # if the value is {None}
            if value is None:
                # chain up
                return super().native(value=value, **kwds)

            # shouldn't get here
            assert False, "unreachable"

    # meta-methods
    def __init__(self, classSlot=None, instanceSlot=None, **kwds):
        # chain up
        super().__init__(**kwds)

        # if the caller has no opinions on what kind of class slots to build
        if classSlot is None:
            # pick one
            # classSlot = self.factory(trait=self, pre=self.process, post=self.process)
            classSlot = self.factory(trait=self, post=self.process)
        # if the caller has no opinions on what kind of instance slots to build
        if instanceSlot is None:
            # pick one
            # instanceSlot = self.factory(trait=self, pre=self.process, post=self.process)
            instanceSlot = self.factory(trait=self, post=self.process)

        # attach
        self.classSlot = classSlot
        self.instanceSlot = instanceSlot

        # all done
        return

    def __str__(self):
        return f"'{self.name}': a property of type '{self.typename}'"


# end of file
