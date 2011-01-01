# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class NodalFieldAccessor:
    """
    Descriptor that provides access to the fields of a record assuming that the values are
    stored in {pyre.calc.Node} compatible objects
    """


    # public data
    index = None # the index of my value in the data tuple
    descriptor = None # the descriptor with the meta data


    # meta methods
    def __init__(self, index, descriptor, **kwds):
        super().__init__(**kwds)
        self.index = index
        self.descriptor = descriptor
        return


    # descriptor interface
    def __get__(self, record, cls):
        """
        Retrieve the value of my field from {record}
        """
        try:
            return record[self.index]
        except TypeError:
            return self.descriptor


    def __set__(self, record, value):
        """
        Store {value} in my {record} field
        """
        # get the descriptor to cast, convert and validate
        value = self.descriptor.process(value)
        # attach it to the node
        record[self.index] = value
        # all done
        return


# end of file 
