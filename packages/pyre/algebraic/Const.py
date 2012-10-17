# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Const:
    """
    Mix-in class that serves a read-only value that must be set during construction
    """

    # interface
    def getValue(self):
        """
        Return my value
        """
        # easy enough
        return self._value


    def setValue(self, value):
        """
        Disable value setting
        """
        # disabled
        raise NotImplementedError("const nodes do not support 'setValue'")


    # meta-methods
    def __init__(self, value, **kwds):
        super().__init__(**kwds)
        self._value = value
        return


    # private data
    _value = None


# end of file 
