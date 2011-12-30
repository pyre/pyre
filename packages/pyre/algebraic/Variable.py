# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Variable:
    """
    Mix-in class to encapsulate nodes that can hold a value.
    """


    # interface
    def getValue(self):
        """
        Return my value
        """
        return self._value


    def setValue(self, value):
        """
        Set my value
        """
        self._value = value
        return


    # meta methods
    def __init__(self, value=None, **kwds):
        super().__init__(**kwds)
        self._value = value
        return


# end of file 
