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

    # Facility is faced with the following problem: the expectations of {pyre_cast} are
    # different depending on whether the object whose trait is being processed is a component
    # class or a component instance. In the latter case, we want to case the trait value into
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
    class instancemaker:
        # types
        from .Component import Component
        # public data
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
                value = value(name="foo")
            # and return it
            return value

        def __init__(self, interface):
            self.interface = interface


    # framework obligations
    def pyre_classSlot(self, evaluator):
        """
        Create a new slot suitable for placing in a component class inventory
        """
        # make a slot with the given {evaluator}
        return self.Slot(processor=self, value=None, evaluator=evaluator)

        
    def pyre_instanceSlot(self, evaluator):
        """
        Create a new slot suitable for placing in a component instance inventory
        """
        # build a value processor
        processor = self.trait()
        # attach a class maker
        processor.type = self.instancemaker(interface=self.type)
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
