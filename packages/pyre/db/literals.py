# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# the handler
class literal:
    """
    A class to encapsulate SQL literals so they can participate in the rendering processes
    """

    # public data
    value = None


    # meta-methods
    def __init__(self, value, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my value
        self.value = value
        # all done
        return

    def __str__(self): return self.value

    def __repr__(self): return self.value

# the constants
null = literal(value='NULL')
default = literal(value='DEFAULT')


# end of file
