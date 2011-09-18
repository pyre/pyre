# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# meta class
from .Mutable import Mutable
# superclass
from .NamedTuple import NamedTuple


# declaration
class DynamicRecord(NamedTuple, metaclass=Mutable):
    """
    Base class for records that have mutable fields.

    Dynamic records are implemented in terms of tuples of {pyre.calc} nodes. As a result, the
    values of their fields may be modified after the initial tuple creation, and all
    derivations are updated dynamically.
    """


    # tuple formation
    @classmethod
    def pyre_processEntries(cls, raw, **kwds):
        """
        Form the tuple that holds my values by extracting information either from {raw} or
        {kwds}, and walking the data through conversion, casting and validation.

        Fields get represented as {pyre.calc.var} instances, while derivations become operators
        on the field nodes.
        """
        # if i were given an explicit tuple, build an iterator over it
        source = iter(raw) if raw is not None else (
            # otherwise, build a generator that extracts values from {kwds}
            kwds.pop(item.name, item.default) for item in cls.pyre_fields
            )
        # build a model
        model = {}
        # now, iterate over my items
        for entry in cls.pyre_entries:
            # build an appropriate node
            node = entry.buildNode(stream=source, model=model)
            # and yield it so it gets placed in my tuple
            yield node
        # all done
        return

        
    # meta methods
    def __new__(cls, raw=None, **kwds):
        """
        Initialize a record using either the pre-qualified tuple {raw}, or by extracting the
        data from {kwds}
        """
        return super().__new__(cls, cls.pyre_processEntries(raw, **kwds))


    def __getitem__(self, index):
        """
        Retrieve the node at {index} and compute its value
        """
        # get the node
        node = super().__getitem__(index)
        # retrieve and return its value
        return node.value


    def __setitem__(self, index, value):
        """
        Retrieve the node at {index} and compute its value
        """
        # find the descriptor responsible for this value
        descriptor = self.pyre_entries[index]
        # get it to cast, convert, validate
        value = descriptor.process(value)
        # get the relevant node
        node = super().__getitem__(index)
        # set its value
        node.value = value
        # and return
        return


    def __iter__(self):
        """
        Iterate over my nodes, returning their value
        """
        # get each of my nodes
        for node in super().__iter__():
            # and return its value
            yield node.value
        # all done
        return


# end of file 
