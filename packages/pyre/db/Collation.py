# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Collation:
    """
    An encapsulation of the collation sequence
    """


    # public data
    field = None
    collation = "ASC"


    # meta methods
    def __init__(self, field, collation=collation, **kwds):
        super().__init__(**kwds)
        self.field = field
        self.collation = collation
        return


    def __str__(self):
        # render the collation specification
        return "{} {}".format(str(self.field), self.collation)


# end of file 
