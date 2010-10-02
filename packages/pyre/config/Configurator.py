# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections
import pyre.tracking


class Configurator:
    """
    The keeper of all configurable values maintained by the framework

    This class is a pyre.calc.AbstractModel that maintains the global configuration state of
    the framework. All configuration events encountered are processed by a Configurator
    instance held by the pyre executive and become nodes in the configuration model.
    """


    # constants
    TRAIT_SEPARATOR = '.'
    FAMILY_SEPARATOR = '#'
    DEFAULT_PRIORITY = (-1, -1)
    EXPLICIT_CONFIGURATION = (15, -1) # programmatic overrides


    # types
    from .Slot import Slot
    from .Model import Model
    # exceptions
    from ..calc.exceptions import (
        CircularReferenceError, DuplicateNodeError, ExpressionError, NodeError,
        UnresolvedNodeError)
    

    # public data
    model = None # the configuration model
    counter = None # the event priority counter
    # build a locator for values that come from trait defaults
    locator = pyre.tracking.newSimpleLocator(source="<defaults>")


    # interface
    def configure(self, configuration, priority):
        """
        Iterate over the {configuration} events and insert them into the model at the given
        {priority} level
        """
        # loop over events
        for event in configuration.events:
            # build the event sequence number, which becomes its priority level
            seq = (priority, self.counter[priority])
            # update the counter
            self.counter[priority] += 1
            # and process the event
            event.identify(inspector=self.model, priority=seq)
        # all done
        return
 

    def slot(self, value, priority=None):
        """
        Build a new slot that holds {value}; 
        """
        # pass the buck to the model
        return self.model.recognize(value=value, priority=priority)


    # framework requests
    def configureComponentClass(self, component):
        """
        Look through the configuration store for nodes that correspond to defaults for the
        traits of the given {component} class and configure them
        """
        # get the class family
        family = component.pyre_family
        # if there is no family name we are done
        if not family: return self
        # get the class inventory
        inventory = component.pyre_inventory

        # MGA
        print("Calculator.configureComponentClass: configuring {!r}, family={!r}".format(
                component.pyre_name, family))
        # inventory
        print("  inventory:")
        for descriptor, slot in inventory.items():
            print("    {.name!r} <- {.value!r}".format(descriptor, slot))
        # let's see what the model knows about {component}
        print("  configuration model:")
        for name, fqname, node in self.model.children(rootKey=family):
            print("    {!r}: {.value!r}".format(name, node))

        # instruct the model to dispatch further access
        self.model.configurables[self.model._hash.hash(family)] = component

        return

        # iterate over all traits, both own and inherited
        for trait in component.pyre_getTraitDescriptors():
            # if this is not configurable trait, skip it
            if not trait.pyre_isConfigurable: continue
            # find the inventory node that corresponds to this trait
            node = inventory[trait]
            # build the canonical name of the trait
            canonical = self.TRAIT_SEPARATOR.join(family + [trait.name])
            # print("  trait: name={!r}, canonical={!r}".format(trait.name, canonical))
            # iterate over all possible names of this trait
            for alias in trait.aliases:
                # print("    alias: {!r}".format(alias))
                # build the key for the target node
                key = self.TRAIT_SEPARATOR.join(family + [alias])
                # print("      looking for {!r}".format(key))
                # look for the matching node
                try:
                    existing = self.findNode(key)
                # if there is no match
                except KeyError:
                    # print("        no such configuration node")
                    # move on to the next node
                    continue # but after the finally clause below!
                # if there is a match
                else:
                    # print("      removing the existing configuration node")
                    # clean up the model by removing the aliased node
                    # the actual value transfer will happen through the call to replace below
                    aliasHash = self._hash.hash(key, separator=self.TRAIT_SEPARATOR)
                    del self._nodes[aliasHash]
                    del self._names[aliasHash]
                # either way, make sure we register this alias with the hash table
                # must be done after the call to findNode, otherwise aliasing will make the
                # node inaccessible
                finally:
                    # print("      aliasing {!r} to {!r}".format(key, canonical))
                    self._hash.alias(alias=key, original=canonical, separator=self.TRAIT_SEPARATOR)
                # print("      processing setting: {!r} <- {!r}".format(alias, existing))
                existing.cede(replacement=node)
            # finally, register the node with the model
            # this must be done after the potential name clash has been prevented by removing all
            # nodes that may be aliases of this one
            self.registerNode(name=canonical, node=node)

        # all done
        return component


    def configureComponentInstance(self, component):
        """
        Initialize the component instance inventory by making the descriptors point to the
        evaluation nodes
        """
        # MGA
        return

        # get the component's family
        family = self.TRAIT_SEPARATOR.join(component.pyre_family)
        # build the component's name
        name = component.pyre_name
        # build the fully qualified name
        fqname = self.FAMILY_SEPARATOR.join(tag for tag in [family,name] if tag)
        # get the component's inventory
        inventory = component.pyre_inventory
        # checkpoint
        # print("Configurator.configureComponentInstance: configuring {!r}, family={!r}".format(
                # component.pyre_name, family))
        # print("  inventory:", inventory)
        # iterate over my traits
        for trait in component.pyre_getTraitDescriptors():
            # skip non-configurable traits
            if not trait.pyre_isConfigurable:
                continue
            # get the node that holds the class default value
            default = component.__class__.pyre_inventory[trait]
            # and its canonical name
            canonical = self.TRAIT_SEPARATOR.join([name, trait.name])
            # print("  trait: name={!r}, canonical={!r}".format(trait.name, canonical))
            # build the authoritative node for this trait
            node = default.newReference()
            # now look for configurations for this trait
            for alias in trait.aliases:
                # print("    alias: {!r}".format(alias))
                # form the name of the potential node
                # first the unqualified name
                uqKey = self.TRAIT_SEPARATOR.join([name, alias])
                # and now the fully qualified name
                fqKey = self.TRAIT_SEPARATOR.join([fqname, alias])
                # for either of these names
                for key in [fqKey, uqKey]:
                    # look for the node
                    # print("      looking for {!r}".format(key))
                    try:
                        existing = self.findNode(key)
                    # if not there
                    except KeyError:
                        # print("      no such configuration node")
                        continue
                    # if the node is there
                    else:
                        # print("      removing the existing configuration node")
                        # clean up the model
                        aliasHash = self._hash.hash(key, separator=self.TRAIT_SEPARATOR)
                        del self._nodes[aliasHash]
                        del self._names[aliasHash]
                    # either way, make sure we register this alias with the has table
                    finally:
                        # print("      aliasing {!r} to {!r}".format(key, canonical))
                        self._hash.alias(
                            alias=key, original=canonical, separator=self.TRAIT_SEPARATOR)
                    # print("      processing setting: {!r} <- {!r}".format(alias, existing))
                    existing.cede(replacement=node)
            # finally, attach the node as an inventory attribute named after the trait
            inventory[trait] = node
            # register it with the model
            self.registerNode(name=canonical, node=node)
        # all done; hand the component back
        return component


    # meta methods
    def __init__(self, executive, name=None, **kwds):
        super().__init__(**kwds)

        # construct my name
        name = name if name is not None else "pyre.configurator"

        # the configuration model
        self.model = self.Model(
            name=name, executive=executive,
            separator=self.TRAIT_SEPARATOR, defaultPriority=self.DEFAULT_PRIORITY)
        # and the event priority counter
        self.counter = collections.Counter()

        return


    def __getitem__(self, name):
        """
        Indexed access of the configuration model
        """
        return self.model[name].value


    def __setitem__(self, name, value):
        """
        Support for programmatic configuration bindings through indexing
        """
        self.model[name] = value
        return


    def dump(self, pattern=None):
        """
        List my contents
        """
        # dump the contents of the configuration model
        self.model.dump()
                
        return


# end of file 
