# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class NodalDerivationAccessor:
    """
    Descriptor that provides access to the fields of a record assuming that the values are
    stored in {pyre.calc.Node} compatible objects
    """


    # public data
    index = None # the index of my value in the data tuple
    descriptor = None # the descriptor with the meta data


    # meta methods
    def __init__(self, index, descriptor):
        self.index = index
        self.descriptor = descriptor
        return


    # descriptor interface
    def __get__(self, record, cls):
        """
        Retrieve the value of my field from {record}
        """
        try:
            return record[self.index].value
        except TypeError:
            return self.descriptor


# end of file 
