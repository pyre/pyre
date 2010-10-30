# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Column:
    """
    Descriptor that iterates over the values of a given sheet comlumn
    """


    # public data
    index = None # the index of this column
    descriptor = None # the original descriptor with the meta data


    # interface
    def column(self, sheet):
        """
        Generate an iterable over the values of this measure in the entire dataset
        """
        # iterate over the entire data set
        for record in sheet.pyre_data:
            # return the values of my measure
            yield record[self.index]
        # all done
        return


    # meta methods
    def __init__(self, index, descriptor, **kwds):
        super().__init__(**kwds)
        self.index = index
        self.descriptor = descriptor
        return


    # descriptor interface
    def __get__(self, sheet, cls):
        """
        Read access to the measure slice from the data set
        """
        # if this instance access
        if sheet is not None:
            # return the column data selector
            return self.column(sheet)
        # otherwise,return the descriptor itself
        return self.descriptor


# end of file 
