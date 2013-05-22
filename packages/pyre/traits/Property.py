# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Slotted import Slotted


class Property(Slotted):
    """
    The base class for attribute descriptors that describe a component's external state
    """


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


    # meta-methods
    def __str__(self):
        return "{0.name}: a property of type {0.schema}".format(self)


# end of file 
