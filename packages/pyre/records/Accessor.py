# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Accessor:
    """
    The object responsible for managing access to record entries
    """


    # public data
    index = None # the index of my value in the data tuple
    entry = None # the associated descriptor with the meta data


    # meta-methods
    def __init__(self, index, entry, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my spot
        self.index = index
        self.entry = entry
        # all done
        return


    def __get__(self, record, cls):
        """
        Entry retrieval
        """
        # if the target of this access is the class itself
        if record is None:
            # just return my meta-data
            return self.entry

        # otherwise, retrieve my item and return it
        return record[self.index]


    def __set__(self, record, value):
        """
        Entry modification
        """
        # try to set the value of this entry; this will fail for const records
        record[self.index] = value
        # all done
        return


# end of file 
