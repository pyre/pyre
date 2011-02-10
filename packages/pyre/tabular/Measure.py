# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..records.Field import Field


class Measure(Field):
    """
    The base class for table descriptors
    """


    # public data in addition to what is inherited from Field
    index = False # True when this measure is a primary key that can be used to create an index


    # interface
    def pyre_sheetColumnAccessor(self, sheet, index):
        """
        Ask the {sheet} for an accessor factory that is appropriate for measures, and use it to
        build an accessor that knows my index in the tuple of items
        """
        # if the user has marked me as a primary key
        if self.index:
            # ask for and return an indexed accessor
            return sheet.pyre_indexedAccessor(index=index, measure=self)

        # otherwise, ask for and return a normal accessor
        return sheet.pyre_measureAccessor(index=index, measure=self)
        


# end of file 
