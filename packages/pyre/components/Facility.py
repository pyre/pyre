# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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

    # Facility is faced with the following problem: the expectations of {pyre_cast} are
    # different depending on whether the object whose trait is being processed is a component
    # class or a component instance. In the latter case, we want to cast the trait value into
    # an actual component instance that is compatible with the facility requireements; in the
    # former we are happy with either a compatible component declaration or an instance

    # In order to pull this off, Facility declares two classes that serve as the processors
    # that are attached to trait slots: one for class traits and another for instance
    # traits. It decides which one to attach to a slot during binding -- see pyre_bindClass and
    # pyre_bindInstance below

    # the descriptor stand-in
    class trait:
        type = None
        validators = ()
        converters = ()

    # the wrapper that creates component instances on {pyre_cast}
    class factory:
        # types
        from .Component import Component
        # public data
        name = None
        interface = None
        # interface
        def pyre_cast(self, value):
            """
            Pass {value} through the interface casting mechanism and instantiate the result
            """
            # if {value} is not an actual instance
            if not isinstance(value, self.Component):
                # let my interface have a pass
                value = self.interface.pyre_cast(value)
                # instantiate it
                value = value(name=self.name)
            # and return it
            return value

        def __init__(self, name, interface):
            self.name = name
            self.interface = interface
            return


    # property overrides
    def pyre_setInstanceTrait(self, instance, value, locator):
        """
        Set this trait of {instance} to value
        """
        # treat it the assignment like a property
        value = super().pyre_setInstanceTrait(instance, value, locator)
        # as a side-effect, the value has been coverted into my native type
        # if, for any reason, that didn't go through
        if not isinstance(value, self.Component):
            # bail
            return value
        # otherwise
        # get the trait slot
        slot = instance.pyre_inventory[self]
        # look up the registration name
        registration = slot._processor.type.name
        # if the two names match, this is an instance that was auto-created by the
        # configuration process
        if registration == value.pyre_name:
            # and there is nothing further to do
            return value
        # otherwise
        # get the configurator
        cfg = instance.pyre_executive.configurator
        # build the namespace
        namespace = registration.split(cfg.TRAIT_SEPARATOR)
        # transfer any deferred configuration settings
        errors = cfg._transferConditionalConfigurationSettings(
            configurable=value, namespace=namespace)
        return value


    # framework obligations
    def pyre_classSlot(self, evaluator):
        """
        Create a new slot suitable for placing in a component class inventory
        """
        # make a slot with the given {evaluator}
        return self.Slot(processor=self, value=None, evaluator=evaluator)

        
    def pyre_instanceSlot(self, name, evaluator):
        """
        Create a new slot suitable for placing in a component instance inventory
        """
        # build a value processor
        processor = self.trait()
        # attach a class maker
        processor.type = self.factory(name=name, interface=self.type)
        # make a slot with the given {evaluator}
        return self.Slot(processor=processor, value=None, evaluator=evaluator)

        
     # meta methods
    def __init__(self, interface, default=None, **kwds):
        super().__init__(**kwds)
        self.type = interface
        self.default = default
        return


    # exceptions
    from .exceptions import FacilitySpecificationError


# end of file 
