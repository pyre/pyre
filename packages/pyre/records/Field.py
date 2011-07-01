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


    # public data
    aliases = None # the set of alternative names by which I am accessible


    # interface
    def pyre_recordFieldAccessor(self, record, index):
        """
        Ask {record} for an accessor factory that is appropriate for fields, and use it to build
        an accessor that knows my index in the tuple of items of {record}
        """
        return record.pyre_fieldAccessor(index=index, field=self)


    def pyre_process(self, value):
        """
        Walk {value} through casting, conversion and validation
        """
        # convert it
        for converter in self.converters:
            value = converter(value)
        # cast it
        value = self.type.pyre_cast(value)
        # validate it
        for validator in self.validators:
            value = validator(value)
        # and return it
        return value


    def pyre_eval(self, *, data, **kwds):
        """
        Extract my value from {data} and walk it through casting, conversion and validation
        """
        # get the value and process it
        return self.pyre_process(value=next(data))


    # meta methods
    def __init__(self, aliases=None, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)
        # initialize my aliases
        self.aliases = set() if aliases is None else aliases
        # all done
        return


# end of file 
