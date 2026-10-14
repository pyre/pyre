# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc

# superclasses
from .Property import Property
from .. import schemata

# support
from .. import tracking

# the maps that hold my values
from .Map import Map
from .KeyMap import KeyMap
from .NameMap import NameMap


# declaration
class Dict(Property, schemata.mapping):
    """
    A property that maps strings to values of the type of its {schema}; the entries of the
    map of a named component live in the configuration store, one per key
    """

    # constants
    typename = "dict"  # the name of my type

    # public data
    @property
    def macro(self):
        """
        The default strategy for handling slot values that are strings and therefore subject to
        some kind of evaluation in the context of the configuration store
        """
        # the text of a whole map is interpolated, whatever the type of its values, and split
        # into entries when the slot is evaluated; each entry is then converted by the slot my
        # schema makes for it
        return self.pyre_nameserver.interpolation

    def native(self, value, **kwds):
        """
        The default strategy for handling macros in slot values
        """
        # if the value is a mapping or an iterable of pairs
        if isinstance(value, collections.abc.Iterable):
            # build a node for each of its entries
            nodes = {key: self.schema.macro(value=load) for key, load in self._entries(value=value)}
            # and attach them to a mapping node
            return self.pyre_nameserver.mapping(nodes, **kwds)
        # anything else, {None} included, is stored in a variable; when it is read, {None} stays
        # {None}, and anything that is not a map is rejected by {coerce}
        return self.pyre_nameserver.variable(value=value, **kwds)

    # my value processors
    def process(self, value, **kwds):
        """
        Walk {value} through the casting procedure appropriate for clients that are component
        classes
        """
        # the entries of the map get class slots
        return super().process(value=value, slots=self.schema.classSlot, **kwds)

    def instantiate(self, value, **kwds):
        """
        Walk {value} through the casting procedure appropriate for clients that are component
        instances
        """
        # the entries of the map get instance slots
        return super().process(value=value, slots=self.schema.instanceSlot, **kwds)

    def coerce(self, value, slots=None, **kwds):
        """
        Convert {value}, a mapping, an iterable of pairs, or text, into a dictionary whose values
        are converted by my {schema}; the factory of the {slots} of the entries is for {deposit}
        """
        # leave the factory out of the conversion of the entries, and convert
        return super().coerce(value=value, **kwds)

    def deposit(self, value, node, slots, **kwds):
        """
        Place the entries of {value}, a dictionary, in slots built by the factory {slots}, and
        hand back the map that holds them
        """
        # build the map
        return self.catalog(factory=slots, entries=value.items(), node=node)

    # framework hooks triggered by client configuration
    def classConfigured(self, component, **kwds):
        """
        Notification that the client class record has been configured
        """
        # chain up
        super().classConfigured(component=component, **kwds)
        # configure the class record
        self.configureClient(client=component, factory=self.classSlot)
        # all done
        return self

    def instanceConfigured(self, instance, **kwds):
        """
        Notification that the client instance has been configured
        """
        # chain up
        super().instanceConfigured(instance=instance, **kwds)
        # configure the instance
        self.configureClient(client=instance, factory=self.instanceSlot)
        # all done
        return self

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dict; an {authority} that does not know dicts sees me as the
        mapping i am
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDict
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # meta-methods
    def __init__(self, schema=None, **kwds):
        # an unspecified schema for my entries is the trait counterpart of the schemata
        # default, made for me alone: entries are passed through as they are
        if schema is None:
            # so make an identity trait
            schema = self.identity()
        # chain up, with slot factories that build maps out of the values of my slots
        super().__init__(
            schema=schema,
            classSlot=self.factory(trait=self, post=self.process),
            instanceSlot=self.factory(trait=self, post=self.instantiate),
            **kwds,
        )
        # all done
        return

    def __get__(self, instance, cls):
        """
        Retrieve my value, introducing the map to the instance that owns it, so that it can
        notify its owner when one of its entries changes
        """
        # get the value
        value = super().__get__(instance, cls)
        # if it is the map of an instance
        if instance is not None and isinstance(value, Map):
            # introduce them
            value.client = instance
        # and hand it off
        return value

    # implementation details
    def catalog(self, factory, entries, node):
        """
        Instantiate an appropriate map and fill it with the (key, value) pairs in {entries}
        """
        # access the store
        nameserver = self.pyre_nameserver
        # get the node key
        key = node.key
        # a node without a key lives outside the store
        if key is None:
            # so its map holds its own slots
            catalog = NameMap(trait=self, factory=factory)
            # and has no metadata of its own
            meta = None
        # otherwise
        else:
            # its entries live in the store, under its name
            catalog = KeyMap(trait=self, factory=factory, key=key)
            # and they carry the priority of the assignment that made the map, so they compete
            # on equal terms with the settings of individual keys
            meta = nameserver.getInfo(key)

        # go through the entries
        for name, setting in entries:
            # a key that holds the separator of the store would name a deeper level of it
            if nameserver.separator in name:
                # so leave it out
                self._skip(entry=name, reason="keys can't hold the separator of the store")
                # and move on
                continue
            # make a locator that leads back to where the map was set
            locator = tracking.chain(
                this=tracking.simple(f"while adding entry '{name}' to '{self.name}'"),
                next=meta.locator if meta is not None else None,
            )
            # and update my map
            catalog.insert(
                name=name,
                value=setting,
                locator=locator,
                priority=meta.priority if meta is not None else None,
            )

        # a map in the store
        if meta is not None:
            # also holds the keys set individually at a priority higher than the map's own
            for child, _ in nameserver.children(key):
                # get the metadata of the setting
                info = nameserver.getInfo(child)
                # settings the map outranks were replaced by it
                if not meta.priority < info.priority:
                    # so skip them
                    continue
                # the others join the map; they were made before my schema was known, so rebuild
                # their slots with my factory, which converts their values; at the priority of
                # the defaults, the store keeps their value, priority and locator
                catalog.insert(
                    name=info.split[-1],
                    value=None,
                    locator=info.locator,
                    priority=nameserver.priority.defaults(),
                )

        # and return it
        return catalog

    def configureClient(self, client, factory):
        """
        Fill the map of a named {client} with the settings that are meant for it
        """
        # access the store
        nameserver = self.pyre_nameserver
        # and the configurator
        configurator = self.pyre_configurator
        # find my slot
        slot = client.pyre_inventory[self]
        # this gets called only for public inventory items, so I am guaranteed a key
        key = slot.key
        # the conditional assignments meant for the client
        deferred = list(configurator.retrieveDeferredAssignments(key=key))

        # get my value, which already holds the keys set individually
        current = slot.value
        # a map that is not there
        if current is None:
            # is made out of the keys set individually, if there are any
            settings = [
                (nameserver.getInfo(child), node) for child, node in nameserver.children(key)
            ]
            # if there are none, and no conditional assignments either
            if not settings and not deferred:
                # the map stays out
                return self
            # otherwise, the map takes the priority and the locator of the strongest of them
            strongest = max(
                [info.priority for info, _ in settings] + [priority for _, priority in deferred]
            )
            # attach a map with the keys set individually
            client.pyre_inventory.setTraitValue(
                trait=self,
                factory=factory,
                value={info.split[-1]: node.value for info, node in settings},
                priority=strongest,
                locator=tracking.simple(f"while configuring '{client.pyre_name}'"),
            )
            # and get it
            current = client.pyre_inventory[self].value

        # go through the conditional assignments
        for assignment, priority in deferred:
            # and add each one to the map
            current.insert(
                name=assignment.key[0],
                value=assignment.value,
                priority=priority,
                locator=assignment.locator,
            )

        # all done
        return self


# end of file
