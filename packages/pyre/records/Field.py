# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# superclasses
from ..algebraic.Node import Node
from ..schema.Descriptor import Descriptor


# declaration
class Field(Descriptor, Node):
    """
    The base class for record descriptors
    """


    # interface
    def pyre_accessor(self, record, index):
        """
        Ask {record} for an accessor factory that it appropriate to fields and use it to build
        one that knows my index in the tuple of items of {record}
        """
        return record.pyre_fieldAccessor(index=index, field=self)


    def pyre_process(self, value):
        """
        Walk {value} through casting, conversion and validation
        """
        # cast it
        value = self.type.pyre_cast(value)
        # convert it
        for converter in self.converters:
            value = converter(value)
        # validate it
        for validator in self.validators:
            value = validator(value)
        # and return it
        return value


    def eval(self, *, data, **kwds):
        """
        Extract my value from {data} and walk it through casting, conversion and validation
        """
        # get the value
        value = next(data)
        # cast it
        value = self.type.pyre_cast(value)
        # convert it
        for converter in self.converters:
            value = converter(value)
        # validate it
        for validator in self.validators:
            value = validator(value)
        # and return it
        return value


# end of file 
