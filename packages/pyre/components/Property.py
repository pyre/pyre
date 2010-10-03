# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections
import pyre.calc
from .Trait import Trait


class Property(Trait):
    """
    The base class for attribute descriptors that describe a component's external state
    """


    # types
    from .Slot import Slot


    # import the packages exposed by properties for convenince
    from .. import schema, constraints


    # public data; inherited from Trait but repeated here for clarity
    name = None # my canonical name; set at construction time or binding name
    aliases = None # the set of alternative names by which I am accessible
    tip = None # a short description of my purpose and constraints; contrast with doc
    # additional state
    type = schema.object # my type; most likely one of the pyre.schema type declarators
    default = None # my default value
    optional = False # am i allowed to be uninitialized?
    converters = () # the chain of functions that are required to produce my native type
    validators = () # the chain of functions that validate my values


    # interface
    def pyre_initialize(self):
        """
        Attach any metadata harvested by the requirement metaclass

        This gets called by Requirement, the metaclass of all configurables, as part of the
        process that constructs the class record. Don't expect {configurable} to be fully
        functioning at this point.
        """
        # do whatever my superclass requires
        super().pyre_initialize()
        # adjust the validators
        if self.validators is not tuple():
            # if the user placed them in a container
            if isinstance(self.validators, collections.Iterable):
                # convert it into a tuple
                self.validators = tuple(trait.validators)
            # otherwise
            else:
                # make a tuple out of the lone validator
                self.validators = (self.validators, )
        # repeat for the converters
        if self.converters is not tuple():
            # if the user placed them in a container
            if isinstance(self.converters, collections.Iterable):
                # convert it into a tuple
                self.converters = tuple(trait.converters)
            # otherwise
            else:
                # make a tuple out of the lone converter
                trait.converters = (trait.converters, )
        # and return
        return self


    def pyre_embedLocal(self, component):
        """
        Initialize the inventory of {component}
        """
        # build a literal evaluator to hold my default value
        evaluator = pyre.calc.literal(value=self.default)
        # build a slot
        slot = self.Slot(descriptor=self, value=None, evaluator=evaluator)
        # attach the slot to the inventory
        component.pyre_inventory[self] = slot
        # and return
        return self


    def pyre_embedInherited(self, component):
        """
        Initialize the {component} inventory by establishing a reference to the nearest
        ancestor that has slot for me
        """
        # loop over my pedigree looking for an ancestor that has a slot for me
        for base in component.pyre_pedigree:
            # if it's here, get the slot and bail out
            try:
                node = base.pyre_inventory[self]
                break
            # if not, get the next
            except KeyError:
                continue
        # impossible: couldn't find the slot; what went worng?
        else:
            import journal
            firewall = journal.firewall("pyre.components")
            raise firewall.log("UNREACHABLE")
            
        # build a reference to the slot
        evaluator = node.newReference()
        # make a slot  out of it
        slot = self.Slot(descriptor=self, value=None, evaluator=evaluator)
        # attach it to the inventory
        component.pyre_inventory[self] = slot
        # and return
        return self

        
    def pyre_bindClass(self, configurable):
        """
        Bind this trait to the {configurable} class record

        This method gets called by the {Executive} after the class record {configurable} has
        been through the configuration process. At this point, the value stored in the
        {pyre_inventory} must be cast to its native type and validated
        """
        # get the node that holds my value
        node = configurable.pyre_inventory[self]
        # extract the cached value and the evaluator
        value = node._value
        evaluator = node._evaluator
        # currently, the expectation is that if the value cache already contains a value, it
        # has already gone through the casting and validation process, so there is nothing
        # further to do.
        if value is not None: return value
        # further, uninitialized traits have None for both the value cache and the evaluator;
        # leave those alone as well
        if value is None and evaluator is None: return None
        # so the only case that we have to handle is a null value in the cache and a non-null
        # evaluator. attempt to get the evaluator to compute the value
        try:
            value = evaluator.compute()
        # re-raise errors associated with unresolved nodes
        except node.UnresolvedNodeError as error:
            error.node = node
            raise
        # dress anything else up as an evaluation error
        except Exception as error:
            raise node.EvaluationError(evaluator=evaluator, error=error) from error
        # walk the computed value through casting and validation
        if value is not None:
            # cast it
            value = self.type.pyre_cast(value)
            # convert it
            for converter in self.converters:
                value = converter.pyre_cast(value)
            # validate it
            for validator in self.validators:
                value = validator(value)

        # place it in the cache
        node._value = value
        # and return it back to the caller
        return value


    def pyre_bindInstance(self, configurable):
        """
        Bind this trait to the {configurable} instance
        """
        # get my value from the inventory of {configurable}
        node = configurable.pyre_inventory[self]
        # get the component factory from the class record
        value = node._value
        evaluator = node._evaluator
        # currently, the expectation is that if the value cache already contains a value, it
        # has aleady gone throught the casting validation and instantiation process, so there
        # is nothing further to do
        if value is not None: return value
        # facilities are not supposed to be uninitialized, so having both value and evaluator
        # be None is an error
        if value is None and evaluator is None:
            raise self.FacilitySpecificationError(
                configurable=configurable, trait=self, value=value)
        # so the only case that we have to handle is a null value in the cache and a non-null
        # evaluator. attempt to get the evaluator to compute the value
        try:
            value = evaluator.compute()
        # re-raise errors associated with unresolved nodes
        except node.UnresolvedNodeError as error:
            error.node = node
            raise
        # dress anything else up as an evaluation error
        except Exception as error:
            raise node.EvaluationError(evaluator=evaluator, error=error) from error
        # walk the computed value through casting and validation
        if value is not None:
            # cast it
            value = self.type.pyre_cast(value)
            # convert it
            for converter in self.converters:
                value = converter.pyre_cast(value)
            # validate it
            for validator in self.validators:
                value = validator(value)
        # place it in the cache
        node._value = value
        # and return it back to the caller
        return value


    # trait access
    def getValue(self, client):
        """
        Retrieve the value of this trait
        """
        # print("Property.getValue: OBSOLETE")
        # first, look through the client's inventory
        try:
            node = client.pyre_inventory[self]
        except KeyError:
            # if that failed, fetch the node with the default value from the class record
            node = client.pyre_getTraitDefaultValue(self)
        # we found the node; get the value
        value = node._value
        # if the value is not None, return it as is; it has already gone through casting and
        # validation and it good to go
        if value: return value
        # otherwise, get the node evaluator
        evaluator = node._evaluator
        # if it is valid
        if evaluator:
            # attempt to get it to produce a value
            try:
                value = evaluator.compute()
            # leave unresoved node errors alone
            except node.UnresolvedNodeError as error:
                error.node = node
                raise
            # dress anything else up as an evaluation error
            except Exception as error:
                raise node.EvaluationError(evaluator=evaluator, error=error) from error
        # at this point, if value is None the trait is uninitialized so return it
        if value is None: return None
        # otherwise, walk it through casting and validation
        # raise NotImplementedError("NYI")
        # and return it
        return value


    # the descriptor interface
    def __get__(self, instance, cls):
        """
        Retrieve the value of this trait
        """
        client = instance if instance else cls
        return self.getValue(client)


    def __set__(self, instance, value):
        """
        Set this trait of {instance} to {value}

        The target {instance} may be a component instance or a component class record. Either
        way, the assignment is performed through the {pyre_inventory} attribute, and the
        property descriptor is unaware of the difference
        """
        return self.setValue(instance, value)


    # FIXME
    # OBSOLETE AND INCORRECT IMPLEMENTATIONS

    def setValue(self, client, value, priority=None, locator=None):
        """
        Set this trait of {client} to value
        """
        # print("Property.setValue: OBSOLETE")
        client.pyre_inventory[self] = self.Slot(value=value, evaluator=None)
        return


# end of file 
