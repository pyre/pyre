# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
        # error accumulator
        errors = []
        # loop over events
        for event in configuration.events:
            # build the event sequence number, which becomes its priority level
            seq = (priority, self.counter[priority])
            # update the counter
            self.counter[priority] += 1
            # and process the event
            # print("pyre.config.Configurator.configure: event=", event)
            event.identify(inspector=self, priority=seq)
        # all done
        return errors
 

    # support for the pyre executive
    def configureComponentClass(self, component):
        """
        Adjust the model for the presence of a component

        Look through the model for settings that correspond to {component} and transfer them to
        its inventory. Register {component} as the handler of future configuration events in
        its namespace
        """
        # get the class family
        ns = component.pyre_family
        # if there is no family name, we are done
        if not ns: return []
        # transfer the configuration under the component's family name
        errors = self._transferConfigurationSettings(configurable=component, namespace=ns)
        # return the accumulated errors
        return errors


    def configureComponentInstance(self, component, name=None):
        """
        Initialize the component instance inventory by making the descriptors point to the
        evaluation nodes
        """
        # build the namespace
        name = name if name is not None else component.pyre_name
        # turn it into a key
        ns = name.split(self.separator)
        # transfer the configuration under the component's name
        errors = self._transferConfigurationSettings(configurable=component, namespace=ns)
        # transfer the deferred configuration
        errors = self._transferConditionalConfigurationSettings(
            configurable=component, namespace=ns, errors=errors)

        # and return
        return errors


    # meta methods
    def __init__(self, executive, name=None, **kwds):
        # construct my name
        name = name if name is not None else "pyre.configurator"
        super().__init__(name=name, executive=executive, separator=self.TRAIT_SEPARATOR, **kwds)

        # the event priority counter
        self.counter = collections.Counter()

        return


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


    # implementation details
    def _transferConfigurationSettings(self, configurable, namespace, errors=None):
        """
        Transfer ownership of the configuration store to {configurable} and apply whatever
        configuration is available for it in the configuration store
        """
        # print("Configurator._transferConfigurationSettings:")
        # print("  configurable={.pyre_name!r}".format(configurable))
        # print("  namespace={!r}".format(namespace))
        # initialize the error accumulator
        errors = errors if errors is not None else []
        # get the inventory
        inventory = configurable.pyre_inventory
        # let's see what is known about this instance
        # print("  looking for configuration settings:")
        for key, name, fqname, node in self.children(rootKey=namespace):
            # print("    found {!r} <- {.value!r}".format(fqname, node))
            # print("      with priority: {._priority}".format(node))
            # find the corresponding descriptor
            try:
                descriptor = configurable.pyre_getTraitDescriptor(alias=name)
                # print("      matching descriptor: {.name!r}".format(descriptor))
            # found a typo?
            except configurable.TraitNotFoundError as error:
                # print("      no matching descriptor")
                errors.append(error)
                continue
            # get the inventory slot
            slot = inventory[descriptor]
            # merge the information
            # print("      before: {0._processor.name!r} <- {0.value!r}".format(slot))
            self.patch(discard=node, keep=slot)
            # print("      after: {0._processor.name!r} <- {0.value!r}".format(slot))
            # patch the model
            # replace the node with the inventory slot so aliases still work
            self._nodes[key] = slot
            # and eliminate the old node from the name stores
            del self._names[key]
            del self._fqnames[key]
        # print("  done with {.pyre_name!r}".format(configurable))
        # establish {component} as the handler of events in its configuration namespace
        self.configurables[self.separator.join(namespace)] = configurable
        # return the accumulated errors
        return errors


    def _transferConditionalConfigurationSettings(self, configurable, namespace, errors=None):
        """
        Apply whatever deferred configuration settings are available in the configuration store
        under {namespace}
        """
        # print("Configurator._transferConditionalConfigurationSettings:")
        # print("  configurable={.pyre_name!r}".format(configurable))
        # print("  namespace={!r}".format(namespace))
        # initialize the error pile
        errors = errors if errors is not None else []
        # get the family name
        family = configurable.pyre_family
        # print("  family={!r}".format(family))
        # if there isn't one, we are all done
        if not family: 
            # print("  no family, bailing out")
            return errors
        # get the inventory
        inventory = configurable.pyre_inventory
        # hash the two to build the deferral key
        ckey = self._hash.hash(namespace)
        fkey = self._hash.hash(family)
        # if there aren't any settings that match these criteria, we are all done
        if (ckey, fkey) not in self.deferred: 
            # print("  no deferred configuration")
            return errors
        # otherwise, loop over the assignments
        for trait, node in self.deferred[(ckey,fkey)]:
            # build the trait name
            alias = self.separator.join(trait)
            # print("    found {!r} <- {.value!r}".format(alias, node))
            # look for the corresponding descriptor
            try:
                descriptor = configurable.pyre_getTraitDescriptor(alias=alias)
                # print("      matching descriptor: {.name!r}".format(descriptor))
            # found a typo?
            except configurable.TraitNotFoundError as error:
                # print("      no matching descriptor")
                errors.append(error)
                continue
            # get the inventory slot
            slot = inventory[descriptor]
            # merge the information
            # MGA: this is not right: what if you have to re-apply these settings on a second
            # assignment to the same trait?
            # print("      before: {0._processor.name!r} <- {0.value!r}".format(slot))
            self.patch(discard=node, keep=slot)
            # print("      after: {0._processor.name!r} <- {0.value!r}".format(slot))

        # print("  done with {.pyre_name!r}".format(configurable))
        # return the accumulated errors
        return errors


# end of file 
