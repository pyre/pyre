# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class ConstAccessor:
    """
    Descriptor that provides access to a record item
    """


    # public data
    index = None # the index of my value in the data tuple
    entry = None # the entry with the meta data


    # meta methods
    def __init__(self, index, entry, **kwds):
        super().__init__(**kwds)
        self.index = index
        self.entry = entry
        return


    # descriptor interface
    def __get__(self, record, cls):
        """
        Retrieve the value of my entry from {record}
        """
        try:
            return record[self.index]
        except TypeError:
            return self.entry


# end of file 
