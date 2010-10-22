# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Accessor:
    """
    Descriptor that provides access to the fields of a record
    """


    # public data
    index = None


    # meta methods
    def __init__(self, index):
        self.index = index
        return


    # descriptor interface
    def __set__(self, record, value):
        """
        Store {value} in my field in {record}
        """
        # index {record} to get my slot and set its value
        record[self.index].value = value
        # all done
        return


    def __get__(self, record, cls):
        """
        Retrieve the value of my field from {record}
        """
        try:
            return record[self.index].value
        except TypeError:
            return self


# end of file 
