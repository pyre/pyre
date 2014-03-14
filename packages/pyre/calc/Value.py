# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


class Value:
    """
    Mix-in class to encapsulate nodes that can hold a value.
    """


    # interface
    def getValue(self, **kwds):
        """
        Return my value
        """
        return self._value


    def setValue(self, value, **kwds):
        """
        Set my value
        """
        # store the value
        self._value = value
        # all done
        return self


    # meta methods
    def __init__(self, value=None, **kwds):
        super().__init__(**kwds)
        self._value = value
        return


    # private data
    _value = None


# end of file 
