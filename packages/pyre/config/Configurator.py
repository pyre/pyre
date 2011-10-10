# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Model import Model


class Configurator(Model):
    """
    The keeper of all configurable values maintained by the framework

    This class is a pyre.calc.AbstractModel that maintains the global configuration state of
    the framework. All configuration events encountered are processed by a Configurator
    instance held by the pyre executive and become nodes in the configuration model.
    """


    # interface
    def configure(self, configuration, priority):
        """
        Iterate over the {configuration} events and insert them into the model at the given
        {priority} level
        """
        # error accumulator
        errors = []
        # loop over events
        for event in configuration:
            # build the event sequence number, which becomes its priority level
            seq = (priority, next(self.counter[priority]))
            # and process the event
            # print("pyre.config.Configurator.configure:", event)
            event.identify(inspector=self, priority=seq)
        # all done
        return errors
 

    # support for the pyre executive
    def configureComponentClass(self, registrar, component):
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
        errors = self._verifyConfigurationSettings(configurable=component, namespace=ns)
        # return the accumulated errors
        return errors


    def configureComponentInstance(self, registrar, component, name=None):
        """
        Initialize the component instance inventory by making the descriptors point to the
        evaluation nodes
        """
        # build the namespace
        name = name if name is not None else component.pyre_name
        # turn it into a key
        ns = name.split(self.separator)
        # transfer the configuration under the component's name
        errors = self._verifyConfigurationSettings(configurable=component, namespace=ns)
        # transfer the deferred configuration
        errors = self._transferConditionalConfigurationSettings(
            registrar=registrar, configurable=component, namespace=ns, errors=errors)

        # and return
        return errors


    # meta methods
    def __init__(self, executive, name=None, **kwds):
        # construct my name
        name = name if name is not None else "pyre.configurator"
        super().__init__(name=name, executive=executive, **kwds)

        return


    # implementation details
    def _verifyConfigurationSettings(self, configurable, namespace, errors=None):
        """
        Verify that the nodes in the configuration store that belong to the {namespace} owned
        by {configurable} are consistent with its set of traits.

        This routine is useful for detecting typos on the command line and package
        configuration files
        """
        # print("Configurator._verifyConfigurationSettings:")
        # print("  configurable={.pyre_name!r}".format(configurable))
        # print("  namespace={!r}".format(namespace))

        # initialize the error accumulator
        errors = errors if errors is not None else []
        # get the inventory
        inventory = configurable.pyre_inventory
        # let's see what is known about this instance
        # print("  looking for configuration settings:")

        # iterate over all settings that are the logical children of the given {namespace}
        for key, slot in self.children(key=namespace):
            # print("    found {0.name!r}, with priority: {0.priority}".format(slot))
            # print("      from: {0.locator}".format(slot))

            # try to find the corresponding descriptor
            # build its name: its the last portion of its full name
            name = slot.name.split(self.separator)[-1]
            # if it is there
            try:
                # get the descriptor
                descriptor = configurable.pyre_getTraitDescriptor(alias=name)
                # print("      matching descriptor: {.name!r}".format(descriptor))
            # found a typo?
            except configurable.TraitNotFoundError as error:
                # print("      no matching descriptor")
                errors.append(error)
                continue
            # consistency check: the slot in the inventory should be the same as the slot in
            # the model; this currently may fail under some aliasing configurations. the
            # firewall should flush these cases out
            if slot is not inventory[descriptor]:
                # print(" ********* FIREWALL ********* ")
                # get the journal
                import journal
                # build a firewall
                firewall = journal.firewall(name="pyre.config")
                # and raise it
                raise firewall.log("slot mismatch for {.name!r}".format(slot))
        # all done
        # print("  done with {.pyre_name!r}".format(configurable))
        # return the accumulated errors
        return errors


    def _transferConditionalConfigurationSettings(
           self,
           registrar, configurable, namespace, errors=None):
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
        # if there aren't any settings that match these criteria, we are all done
        if ckey not in self.deferred: 
            # print("  no deferred configuration")
            return errors

        # otherwise, loop over the assignments
        for assignment, priority in self.deferred[ckey]:
            # build the trait name
            alias = self.separator.join(assignment.key)
            # print("    found: {!r} <- {.value!r}".format(alias, assignment))
            # print("      from", assignment.locator)
            # print("      with priority", priority)
            # make sure all the conditions apply
            match = False
            # print("    conditions:")
            for name, family in assignment.conditions:
                # print("      name={}, family={}".format(name, family))
                # if the name matches the given {namespace},
                if name == namespace:
                    # print("      namespace match")
                    target = configurable
                # otherwise, look for a registered component by that name
                else:
                    # print("      looking up by name...")
                    try:
                        target = registrar.names[self.separator.join(name)]
                        # print("        got it")
                    # no match
                    except KeyError:
                        # print("        not there")
                        # and search no more
                        break
                # bail out if the families don't match
                if target.pyre_family != family: 
                    # print("      families don't match")
                    break
                # otherwise
                # print("      families match")
            # if we didn't exit prematurely, it's a match
            else:
                match = True
                
            # if no match
            if not match:
                # move on to the next one
                continue

            # print("    all conditions passed")
            # look for the corresponding descriptor
            try:
                descriptor = configurable.pyre_getTraitDescriptor(alias=alias)
                # print("    matching descriptor: {.name!r}".format(descriptor))
            # found a typo?
            except configurable.TraitNotFoundError as error:
                # print("    no matching descriptor")
                errors.append(error)
                continue

            # find the slot
            slot = configurable.pyre_inventory[descriptor]

            # assign the trait value
            # print("    before: {!r} <- {!r}".format(alias, getattr(configurable, alias)))
            self._assign(
                existing=slot, value=assignment.value,
                priority=priority, locator=assignment.locator) 
            # print("    before: {!r} <- {!r}".format(alias, getattr(configurable, alias)))

        # print("  done with {.pyre_name!r}".format(configurable))
        # return the accumulated errors
        return errors


# end of file 
