# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections
import pyre.tracking
from .Model import Model


class Configurator(Model):
    """
    The keeper of all configurable values maintained by the framework

    This class is a pyre.calc.AbstractModel that maintains the global configuration state of
    the framework. All configuration events encountered are processed by a Configurator
    instance held by the pyre executive and become nodes in the configuration model.
    """


    # constants
    TRAIT_SEPARATOR = '.'
    FAMILY_SEPARATOR = '#'

    # exceptions
    from ..calc.exceptions import (
        CircularReferenceError, DuplicateNodeError, ExpressionError, NodeError,
        UnresolvedNodeError)
    

    # public data
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
            event.identify(inspector=self, priority=seq)
        # all done
        return
 

    # support for the pyre executive
    def configureComponentClass(self, component):
        """
        Adjust the model for the presence of a component

        Look through the model for settings that correspond to {component} and transfer them to
        its inventory. Register {component} as the handler of future configuration events in
        its namespace
        """
        # the accumulator of error
        errors = []
        # get the class family
        family = component.pyre_family
        # if there is no family, we are done
        if not family: return errors
        # get the class inventory
        inventory = component.pyre_inventory
        # let's see what is known about {component}
        for key, name, fqname, node in self.children(rootKey=family):
            # find the corresponding descriptor
            try:
                descriptor = component.pyre_getTraitDescriptor(alias=name)
            # found a typo?
            except component.TraitNotFoundError as error:
                errors.append(error)

            # get the inventory slot
            slot = inventory[descriptor]
            # merge the slots
            slot.merge(other=node)
            # patch me
            self.patch(old=node, new=slot)
            # replace the node with the inventory slot so aliases still work
            self._nodes[key] = slot
            # and eliminate the old node from the name stores
            del self._names[key]
            del self._fqnames[key]
        # establish {component} as the handler of events in its configuration namespace
        self.configurables[self.separator.join(family)] = component
        # return the accumulated errors
        return errors


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
        # construct my name
        name = name if name is not None else "pyre.configurator"
        super().__init__(name=name, executive=executive, separator=self.TRAIT_SEPARATOR, **kwds)

        # the event priority counter
        self.counter = collections.Counter()

        return


    def __getitem__(self, name):
        """
        Indexed access to the configuration store
        """
        return self.resolve(name=name).value


    def __setitem__(self, name, value):
        """
        Support for programmatic modification of the configuration store
        """
        # get the priority sequence class for explicit settings
        explicit = self.executive.EXPLICIT_CONFIGURATION
        # build the event sequence number, which becomes its priority level
        seq = (explicit, self.counter[explicit])
        # update the counter
        self.counter[explicit] += 1
        # build a slot
        slot = self.nodeFactory(value=None, evaluator=self.recognize(value=value), priority=seq)
        # build a locator
        locator = pyre.tracking.here(level=1)
        # register the slot
        self.register(name=name, node=slot)
        # and return
        return


# end of file 
