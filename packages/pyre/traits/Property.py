# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import collections
from .. import schema
from .. import tracking

# superclass
from .Slotted import Slotted


class Property(Slotted):
    """
    The base class for attribute descriptors that describe a component's external state
    """


    # public data
    schema = schema.identity # inherited from {Descriptor}
    converters = () # the chain of functions that are required to produce my native type
    normalizers = () # the chain of functions that convert my values to canonical form
    validators = () # the chain of functions that validate my values


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
        value = self.schema.coerce(value, **kwds)
        # normalize
        for normalizer in self.normalizers: value = normalizer(value)
        # validate
        for validator in self.validators: value = validator(value)
        # and return the new value
        return value


    # framework support
    def attach(self, **kwds):
        """
        Attach any metadata harvested by the requirement metaclass

        This gets called by {Requirement}, the metaclass of all configurables, as part of the
        process that constructs the class record.
        """
        # chain up
        super().attach(**kwds)
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


    # meta-methods
    def __str__(self):
        return "{0.name}: a property of type {0.schema}".format(self)


# end of file 
