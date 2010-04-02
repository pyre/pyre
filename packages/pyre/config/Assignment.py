# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Event import Event


class Assignment(Event):
    """
    """


    # public data
    key = None
    value = None


    # meta methods
    def __init__(self, key, value, **kwds):
        super().__init__(**kwds)
        self.key = key
        self.value = value
        return


    def __str__(self):
        return "{{{0.key} <- {0.value}}}".format(self)


# end of file 
