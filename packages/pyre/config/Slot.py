# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# my metaclass: defined in the package initialization file
from . import _metaclass_Slot

# slots are {pyre.algebraic} nodes
from ..algebraic.AbstractNode import AbstractNode
# access to the node algebra mix-ins
from ..algebraic.Number import Number
# access to the structural mix-ins
from ..algebraic.Leaf import Leaf
from ..algebraic.Composite import Composite
# access to the functional mix-ins
from ..algebraic.Literal import Literal
from ..algebraic.Variable import Variable
from ..algebraic.Operator import Operator
from ..algebraic.Expression import Expression
from ..algebraic.Interpolation import Interpolation
from ..algebraic.Reference import Reference
from ..algebraic.Unresolved import Unresolved
# evaluation strategies
from ..algebraic.Cast import Cast
from .Memo import Memo

# grab the default priority definition
from .levels import DEFAULT_CONFIGURATION


# class declaration
class Slot(AbstractNode, Memo, Cast, Number, metaclass=_metaclass_Slot):
    """
    This class provides centralized access to the values of configurable traits

    All configuration information recovered from the command line, configuration files or
    explicit assignments to the {configurator} is contained in slots. The {configurator}
    maintains a map from a hashed version of the public name of the value to a slot.

    Similarly, all component classes and instances store the values of their properties and
    facilities in slots. The {pyre_inventory} dictionary is a map from trait descriptors to the
    corresponding slot, and the {__get__} and {__set__} descriptor methods manipulate the slot
    contents.

    Component classes and instances that have public names, {pyre_family} for classes and
    {pyre_name} for instances, register their slots with the {configurator}, which establishes
    the connection between component configurable state and the configuration store. These
    slots are shared among the component and the store, and changes to one are immediately
    reflected in the other.

    In addition, slots manage the trait values by walking them through coercions and
    validations whenever a value change is detected.

    In order to allow configuration assignments to properly override existing values, slots
    maintain the notion of the priority of their current value. This way clients can check
    whether the incoming value may or may not override the existing one. This frees the
    framework from having to guarantee that the configuration store is visited in some fixed
    order.

    Slots also maintain a locator, an indication of the source of the configuration information
    that was used to set the value of the trait.
    """


    # types: hooks for implementing the expression graph construction
    # structural
    leaf = Leaf
    composite = Composite
    # functional; they will be patched below with my subclasses
    literal = None
    variable = None
    operator = None
    expression = None
    interpolation = None
    reference = None
    unresolved = None
    
    # public data
    # access to my value
    @property
    def value(self):
        """
        Get my value
        """
        return self.getValue()

    @value.setter
    def value(self, value):
        """
        Set my value
        """
        # disable this for now
        raise NotImplementedError(
            "class {.__name__!r} does not permit explicit value setting".format(type(self)))
    
    # value meta data
    key = None # the hash key used by the configurator to retrieve this slot
    name = None # the name under which I am registered
    locator = None # the provenance of my value
    priority = (DEFAULT_CONFIGURATION, -1)
    trait = None # the trait descriptor whose value i manage
    processor = None # the processor used by {Cast} to normalize my value


    # interface
    def setValue(self, value):
        """
        Set my value using {value} if this action has high enough priority

        Assumes that the new value has already been converted into a slot. If both {value} and
        i are variables, i will just update my value and the associated meta data; otherwise, i
        will have {value} take my place in the configuration store.
        """
        # ignore the assignment if its {priority} is less than mine
        if value.priority < self.priority: return self
        # if we are both variables
        if isinstance(self, self.variable) and isinstance(value, self.variable):
            # transfer the value
            super().setValue(value=value.value)
            # the priority
            self.priority = value.priority
            # the provenance
            self.locator = value.locator
            # and return
            return self

        # otherwise, transfer my meta-data
        value.key = self.key
        value.name = self.name
        value.trait = self.trait
        value.processor = self.processor
        # let {value} take on all my configurational responsibilities
        value.subsume(self)
        # and return
        return value


    def __init__(self, name=None, key=None, processor=None, locator=None, **kwds):
        super().__init__(**kwds)
        self.key = key
        self.name = name
        self.locator = locator
        self.processor = processor
        return


    # debugging support
    def dump(self):
        print("slot:", self)
        print("  name: {.name}".format(self))
        print("  key: {.key}".format(self))
        print("  trait: {.trait}".format(self))
        print("  configurator: {.configurator}".format(self))
        print("  component class: {.componentClass}".format(self))
        print("  component instance: {.componentInstance}".format(self))
        print("  observers: {.observers}".format(self))


# slot subclasses that close its algebra
# variables
class variable(Slot, Variable, Slot.leaf):
    """
    Concrete class for encapsulating the user accessible nodes
    """
# literals
class literal(Slot, Literal, Slot.leaf):
    """
    Concrete class for representing foreign values
    """
# operators
class operator(Slot, Operator, Slot.composite):
    """
    Concrete class for encapsulating operations among nodes
    """
# expressions
class expression(Slot, Expression, Slot.composite):
    """
    Concrete class for encapsulating macros
    """
# interpolations
class interpolation(Slot, Interpolation, Slot.composite):
    """
    Concrete class for encapsulating macros
    """
# references
class reference(Slot, Reference, Slot.composite):
    """
    Concrete class for encapsulating references to other nodes
    """
# unresolved nodes
class unresolved(Slot, Unresolved, Slot.leaf):
    """
    Concrete class for representing unknown nodes
    """

# patch the base class
Slot.literal = literal
Slot.variable = variable
Slot.operator = operator
Slot.expression = expression
Slot.interpolation = interpolation
Slot.reference = reference
Slot.unresolved = unresolved


# end of file 
