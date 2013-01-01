# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access to the algebraic package
from .. import algebraic
# access to the locators
from .. import tracking
# my metaclass
from . import _metaclass_Slot



# class declaration
class Slot(algebraic.AbstractNode, algebraic.Arithmetic, metaclass=_metaclass_Slot):
    """
    This class provides centralized access to the values of configurable traits

    All configuration information recovered from the command line, configuration files or
    explicit assignments to the {configurator} is contained in slots. The {configurator}
    maintains a map from a hashed version of the public name of the value to a slot.

    Similarly, all component classes and instances store the values of their properties and
    facilities in slots. The {pyre_inventory} dictionary is a map from trait descriptors to the
    corresponding slot, and the {__get__} and {__set__} descriptor methods manipulate the slot
    contents.

    Component classes and instances that have public names register their slots with the
    {configurator}, which establishes the connection between component configurable state and
    the configuration store. These slots are shared among the component and the store, and
    changes to one are immediately reflected in the other.

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


    # types
    # priorities
    from .Priority import Priority as priorities

    # hooks for implementing the expression graph construction
    # structural
    leaf = algebraic.Leaf
    literal = algebraic.Literal
    composite = algebraic.Composite
    const = algebraic.Const
    # evaluation strategies
    memo = algebraic.Memo
    converter = algebraic.Converter
    observer = algebraic.Observer
    observable = algebraic.Observable

    # functional; they will be patched below with my subclasses
    variable = None
    operator = None
    expression = None
    interpolation = None
    reference = None
    unresolved = None

    # constants
    defaultPriority = priorities.defaults

    # public data
    locator = None # the provenance of my value
    priority = None # the priority of the value assignment operation


    # support for value management
    def replace(self, obsolete):
        """
        Take ownership of any information held by the {obsolete} node, which is about to be
        destroyed
        """
        # print("Slot.replace: NYI! not sure what though...")
        return super().replace(obsolete)


    # implementation support
    @classmethod
    def coerce(cls, **kwds):
        raise NotImplementedError("NYI! maybe DNI...")


    @classmethod
    def select(cls, model, existing, replacement):
        """
        Pick either {existing} or {replacement} as the node that will remain in {model}
        """
        # compare the priorities
        if existing.priority > replacement.priority:
            # the existing one wins
            return existing
        # otherwise
        return super().select(model=model, existing=existing, replacement=replacement)


    # meta-methods
    def __init__(self, key, priority, locator, **kwds):
        assert isinstance(priority, self.priorities)
        # chain up
        super().__init__(**kwds)
        # save my state
        self.key = key
        self.locator = locator
        self.priority = priority
        # all done
        return


    # debugging support
    def dump(self, name, indent=""):
        super().dump(indent=indent, name=name)
        print('{}  locator: {}'.format(indent, self.locator))
        print('{}  priority: {}'.format(indent, self.priority))
        return


# literals
class literal(Slot.const, Slot.literal, Slot):
    """
    Concrete class for representing foreign values
    """

# variables
class variable(Slot.memo, Slot.converter, Slot.observable, algebraic.Variable, Slot.leaf, Slot):
    """
    Concrete class for encapsulating the user accessible nodes
    """

# operators
class operator(Slot.memo, Slot.converter, Slot.observer, algebraic.Operator, Slot.composite, Slot):
    """
    Concrete class for encapsulating operations among nodes
    """
    # meta-methods
    def __init__(self, **kwds):
        super().__init__(
            key=None,
            priority=self.priorities.uninitialized(), locator=tracking.here(2),
            **kwds)
        return

# expressions
class expression(
    Slot.memo, Slot.converter, Slot.observer, algebraic.Expression, Slot.composite, Slot):
    """
    Concrete class for encapsulating macros
    """

    def __str__(self): return "expression {.expression!r}".format(self)

# interpolations
class interpolation(
    Slot.memo, Slot.converter, Slot.observer, algebraic.Interpolation, Slot.composite, Slot):
    """
    Concrete class for encapsulating simple string interpolation
    """

    def __str__(self): return "expression {.expression!r}".format(self)

# references
class reference(
    Slot.memo, Slot.converter, Slot.observer, algebraic.Reference, Slot.composite, Slot):
    """
    Concrete class for encapsulating references to other nodes
    """

    def __str__(self): return "reference to {}".format(self.operands[0])

# unresolved nodes
class unresolved(Slot.observable, algebraic.Unresolved, Slot.leaf, Slot):
    """
    Concrete class for representing unknown nodes
    """
    # meta-methods
    def __init__(self, **kwds):
        super().__init__(priority=self.priorities.uninitialized(), locator=None, **kwds)
        return


# patch the base class
Slot.literal = literal
Slot.variable = variable
Slot.operator = operator
Slot.expression = expression
Slot.interpolation = interpolation
Slot.reference = reference
Slot.unresolved = unresolved


# end of file 
