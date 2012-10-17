# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import collections
from .. import tracking

# superclass
from .Slotted import Slotted


class Property(Slotted):
    """
    The base class for attribute descriptors that describe a component's external state
    """


    # convenience: import the packages exposed by properties
    from .. import schema, constraints

    # public data
    converters = () # the chain of functions that are required to produce my native type
    normalizers = () # the chain of functions that convert my values to canonical form
    validators = () # the chain of functions that validate my values

    # framework data; for internal purposes
    isConfigurable = True # properties and subclasses are accessible through {configurator}


    # interface
    def coerce(self, value, **kwds):
        """
        Walk {value} through the casting procedure
        """
        # {None} is special; leave it alone
        if value is None: return None
        # otherwise, convert
        for converter in self.converters: value = converter(value)
        # cast
        value = self.schema.coerce(value)
        # normalize
        for normalizer in self.normalizers: value = normalizer(value)
        # validate
        for validator in self.validators: value = validator(value)
        # and return the new value
        return value


    # framework support
    def initialize(self, **kwds):
        """
        Attach any metadata harvested by the requirement metaclass

        This gets called by {Requirement}, the metaclass of all configurables, as part of the
        process that constructs the class record.
        """
        # chain up
        super().initialize(**kwds)
        # adjust the validators
        if self.validators is not tuple():
            # if the user placed them in a container
            if isinstance(self.validators, collections.Iterable):
                # convert it into a tuple
                self.validators = tuple(self.validators)
            # otherwise
            else:
                # make a tuple out of the lone validator
                self.validators = (self.validators, )
        # repeat for the converters
        if self.converters is not tuple():
            # if the user placed them in a container
            if isinstance(self.converters, collections.Iterable):
                # convert it into a tuple
                self.converters = tuple(self.converters)
            # otherwise
            else:
                # make a tuple out of the lone converter
                self.converters = (self.converters, )
        # and the normalizers
        if self.normalizers is not tuple():
            # if the user placed them in a container
            if isinstance(self.normalizers, collections.Iterable):
                # convert it into a tuple
                self.normalizers = tuple(self.normalizers)
            # otherwise
            else:
                # make a tuple out of the lone normalizer
                self.normalizers = (self.normalizers, )
        # and return
        return self


# end of file 
