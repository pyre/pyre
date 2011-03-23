# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import weakref
import collections
from pyre.calc.HierarchicalModel import HierarchicalModel


class Model(HierarchicalModel):
    """
    A specialization of a hierarchical model that takes into account that the model nodes have
    priorities attached to them and cannot indiscriminately replace each other
    """


    # types
    from .Slot import Slot as nodeFactory


    # interface obligations from HierarchicalModel
    def register(self, *, node, name=None, key=None):
        """
        Add {node} into the model and make it accessible through {name}

        Either {name} or {key} must be non-nil.

        If the optional argument {key} is provided, it will be used to generate the hash key;
        otherwise {name} will be split using the model's field separator. If {key} is supplied
        but {name} is not, an appropriate name will be constructed by splicing together the
        names in {key} using the model's field separator.
        """
        # print("pyre.config.Model.register: name={!r}, key={!r}".format(name, key))
        # build the name
        name = name if name is not None else self.separator.join(key)
        # build the key
        key = tuple(key) if key is not None else name.split(self.separator)
        # build the namespace key and name
        nskey = key[:-1]
        nsname = self.separator.join(nskey)
        item = key[-1]
        # check whether this namespace is known
        try:
            component = self.configurables[nsname]
        # nope: register it as a normal node
        except KeyError:
            return super()._register(
                name=item, fqname=name, node=node, hashkey=self._hash.hash(key))
        # we have a component: treat the name as a property
        descriptor = component.pyre_getTraitDescriptor(alias=item)
        # get the corresponding inventory slot
        slot = component.pyre_inventory[descriptor]
        # merge the two
        slot.merge(other=node)
        # all done
        return self


    def resolve(self, *, name=None, key=None):
        """
        Find the named node

        Either {name} or {key} must be non-nil.

        If the optional argument {key} is provided, it will be used to generate the hash key;
        otherwise {name} will be split using the model's field separator. If {key} is supplied
        but {name} is not, an appropriate name will be constructed by splicing together the
        names in {key} using the model's field separator.
        """
        # print("pyre.config.Model.resolve: name={!r}, key={!r}".format(name, key))
        # build the name
        name = name if name is not None else self.separator.join(key)
        # build the key
        key = key if key is not None else name.split(self.separator)
        # build the namespace key and name
        nskey = key[:-1]
        nsname = self.separator.join(nskey)
        item = key[-1]
        # check whether this namespace is known
        try:
            component = self.configurables[nsname]
        # nope: resolve it as a normal node
        except KeyError:
            return super()._resolve(name=item, fqname=name, hashkey=self._hash.hash(key))
        # we have a component: treat the name as a property
        descriptor = component.pyre_getTraitDescriptor(alias=item)
        # and return the corresponding inventory slot
        return component.pyre_inventory[descriptor]


    # interface for my configurator
    # configuration event processing
    def bind(self, key, value, priority=None, locator=None):
        """
        Build a node with the given {priority} to hold {value}, and register it under {key}
        """
        # build a new node 
        slot = self.nodeFactory(
            value=None, evaluator=self.recognize(value=value), priority=priority, locator=locator)
        # get it registered
        return self.register(node=slot, key=key)


    def defer(self, assignment, priority):
        """
        Build a node that corresponds to a conditional configuration
        """
        # print("Model.defer:")
        # print("    component={}".format(component))
        # print("    conditions={}".format(conditions))
        # print("    key={}, value={!r}".format(key, value))
        # print("    from {}".format(locator))
        # print("    with priority {}".format(priority))
        # hash the component name
        ckey = self._hash.hash(assignment.component)
        # build a slot
        slot = self.nodeFactory(
            value=None, 
            evaluator=self.recognize(value=assignment.value),
            priority=priority, locator=assignment.locator)

        # get the deferred event store and add the event and the slot to the pile
        model = self.deferred[ckey].append( (assignment, slot) )

        # all done
        return slot


    def execute(self, command, priority, locator):
        """
        Record a request to execute a command
        """
        # record the command and its context
        self.commands.append((priority, command, locator))
        # all done
        return self


    def load(self, source, locator, **kwds):
        """
        Ask the pyre {executive} to load the configuration settings in {source}
        """
        # get the executive to kick start the configuration loading
        self.executive.loadConfiguration(uri=source, locator=locator)
        # and return
        return self


    # meta methods
    def __init__(self, executive, **kwds):
        super().__init__(**kwds)
        # record the executive
        self.executive = weakref.proxy(executive)
        # the list of command requests
        self.commands = []
        # the database of deferred bindings
        self.deferred = collections.defaultdict(list)
        # the configurables that manage their own namespace
        self.configurables = weakref.WeakValueDictionary()
        # done
        return


    def dump(self, pattern=None):
        super().dump(pattern)
        if self.configurables:
            print("  configurables:")
            for name in self.configurables:
                print("    {!r}".format(name))
        return


# end of file 
