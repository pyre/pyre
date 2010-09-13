# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Property import Property


class Facility(Property):
    """
    The base class for traits that must coform to a given interface
    """


    # public data; inherited from Trait but repeated here for clarity
    name = None # my canonical name; set at construction time or binding name
    configurable = None # the class where my declaration was found
    aliases = None # the set of alternative names by which I am accessible
    tip = None # a short description of my purpose and constraints; contrast with doc
    # additional state
    type = None # my type; must be an Interface instance
    default = None # my default value
    optional = False # am i allowed to be uninitialized?
    converters = () # the chain of functions that are required to produce my native type
    validators = () # the chain of functions that validate my values


    # binding interface
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
        # cast it
        value = self.type.pyre_cast(value)
        # {value} is now supposed to be a specification for a {Component} subclass
        # instantiate it using the full name of the trait
        value = value(name=configurable.pyre_getTraitFullName(self.name))
        # place it in the cache
        node._value = value
        # and return it back to the caller
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
