# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import weakref


class Index:
    """
    Accessor that assumes the corresponding measure is a primary key and builds an index for it
    """


    # public data
    index = None # the index of this column
    measure = None # the original descriptor with the meta data


    # types
    class keymap(dict):
        """Class that hides the indexing implementation details"""

        def __init__(self, sheet, column, **kwds):
            super().__init__(**kwds)
            self.column = column
            self.sheet = weakref.proxy(sheet)
            return

        def __getitem__(self, key):
            recordIdx = super().__getitem__(key)
            return self.sheet.pyre_data[recordIdx]


    # meta methods
    def __init__(self, index, entry, **kwds):
        super().__init__(**kwds)
        self.index = index
        self.measure = entry
        return


    # descriptor interface
    def __get__(self, sheet, cls):
        """
        Read access to the measure slice from the data set
        """
        # if this instance access
        try:
            # locate the associated keymap and return it to the caller
            # careful here: typos in the name of the keymap storage look normal
            return sheet.pyre_keymaps[self]
        # otherwise
        except AttributeError:
            # return the descriptor itself
            return self.measure


# end of file 
