# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Variable:
    """
    Mix-in class to encapsulate nodes that can hold a value.
    """


    # public data
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        return


    # meta methods
    def __init__(self, value=None, **kwds):
        super().__init__(**kwds)
        self._value = value
        return


# end of file 
