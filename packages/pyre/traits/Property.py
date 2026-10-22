# -*- python -*-
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

    # exceptions
    from ..components.exceptions import StraySettingError

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
            # a non-empty map is not a sequence of its keys
            if isinstance(value, collections.abc.Mapping) and value:
                # so keep it whole, for my schema to refuse when it is read
                return super().native(value=value, **kwds)
            # if the value is a sequence
            if isinstance(value, collections.abc.Iterable):
                # convert the items into nodes
                nodes = (self.schema.macro(value=item) for item in value)
                # and attach them to a sequence node
                return self.pyre_nameserver.sequence(nodes=nodes, **kwds)
            # anything else, {None} or a value that is not a sequence, is kept whole, for my
            # schema to accept or refuse when it is read
            return super().native(value=value, **kwds)

    # framework hooks triggered by client configuration
    def classConfigured(self, component, **kwds):
        """
        Notification that the client class record has been configured
        """
        # chain up
        super().classConfigured(component=component, **kwds)
        # report the settings below my name, which can't reach my value
        self.reportSettingsBelow(client=component)
        # all done
        return self

    def instanceConfigured(self, instance, **kwds):
        """
        Notification that the client instance has been configured
        """
        # chain up
        super().instanceConfigured(instance=instance, **kwds)
        # report the settings below my name, which can't reach my value
        self.reportSettingsBelow(client=instance)
        # all done
        return self

    def reportSettingsBelow(self, client):
        """
        Record against {client} each setting filed below my name: i take none, so none of them
        can reach my value
        """
        # get the store
        nameserver = self.pyre_nameserver
        # and the executive, which keeps the record
        executive = self.pyre_executive
        # find the key of my slot; this gets called only for public inventory items, so there is
        # one
        key = client.pyre_inventory[self].key
        # go through the settings below it, at any depth
        for child, _ in nameserver.descendants(key=key):
            # make an error that names the setting, where it was made, and me
            error = self.StraySettingError(
                configurable=client,
                trait=nameserver.getInfo(key).name,
                setting=nameserver.getInfo(child).name,
                typename=self.typename,
                locator=nameserver.getInfo(child).locator,
            )
            # and record it against {client}
            executive.recordConfigurationError(error=error, configurable=client)
        # all done
        return self

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
