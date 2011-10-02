# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..records.Entry import Entry


class Measure(Entry.variable):
    """
    The base class for table descriptors whose values are explicitly specified in the data source
    """


    # public data in addition to what is inherited from Field
    index = False # True when this measure is a primary key that can be used to create an index


# end of file 
