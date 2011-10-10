# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Property import Property


class Facility(Property):
    """
    The base class for traits that must conform to a given interface
    """

    # public data; look in Property for inherited attributes
    type = None # my type; must be an Interface class record (an instance of Role)
    optional = False # facilities must be given values


    # types
    from .Component import Component

    # Facility is faced with the following problem: the expected result of casting are
    # different depending on whether the object whose trait is being processed is a component
    # class or a component instance. In the latter case, we want to cast the trait value into
    # an actual component instance that is compatible with the facility requirements; in the
    # former we are happy with either a compatible component declaration or an instance.
    # Properties don't have this problem, since they ostensibly represent simple types that can
    # be instantiated without substantial penalty for both component classes and their
    # instances.

    # Normally, conversions of configuration settings to appropriate inventory values is
    # handled by a trait's type. For facilities, this is normally a subclass of
    # {Interface}. {Interface.pyre_cast} solves the first half of the problem: converting a
    # value in to a component class record. In order to solve the second half, {Facility}
    # registers its {pyre_instantiate} as the slot value processor for traits bound to
    # component instances.


    # property overrides
    def pyre_bindInstance(self, configurable):
        """
        Bind this facility to the {configurable} instance
        """
        # get my slot from the {configurable}
        slot = configurable.pyre_inventory[self]
        # attach my value processor
        slot.processor = self.pyre_instantiate
        # mark the slot as dirty
        slot.dirty = True
        # to force it to recompute its value
        return slot.getValue()


    def pyre_instantiate(self, node, value):
        """
        Convert {value} into a component instance
        """
        # if {value} is not an actual instance
        if not isinstance(value, self.Component):
            # let my interface have a pass
            value = self.pyre_cast(node=node, value=value)
            # instantiate it
            value = value(name=node.name)
        # and return it
        return value


    def pyre_setInstanceTrait(self, instance, value, locator):
        """
        Set this trait of {instance} to value
        """
        # treat the assignment like a property
        slot = super().pyre_setInstanceTrait(instance, value, locator)
        # as a side-effect, the value of the slot has been converted into my native type
        component = slot.value
        # if, for any reason, that didn't go through
        if not isinstance(component, self.Component):
            # bail
            return component
        # otherwise
        # look up the registration name
        registration = slot.name
        # if the two names match, this is an instance that was auto-created by the
        # configuration process
        if registration == component.pyre_name:
            # and there is nothing further to do
            return value
        # otherwise
        # get the configurator
        cfg = instance.pyre_executive.configurator
        # get the registrar
        registrar = instance.pyre_executive.registrar
        # build the namespace
        namespace = registration.split(cfg.separator)
        # transfer any deferred configuration settings
        errors = cfg._transferConditionalConfigurationSettings(
            registrar=registrar, configurable=component, namespace=namespace)
        # and return the freshly configured instance
        return value


     # meta methods
    def __init__(self, interface, default=None, **kwds):
        super().__init__(**kwds)
        self.type = interface
        self.default = default
        return


    # exceptions
    from .exceptions import FacilitySpecificationError


# end of file 
