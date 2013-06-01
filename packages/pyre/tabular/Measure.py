# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .. import records
from .. import schemata


# declaration
@schemata.typed
class Measure(records.measure):
    """
    Base class for the measures in this package
    """


    # public data
    indexed = False # {True} when this measure is a primary key used to create an index


    # interface
    def primary(self):
        """
        Mark this measure as a primary key
        """
        # mark me
        self.indexed = True
        # and return me so I chain properly
        return self


# end of file 
