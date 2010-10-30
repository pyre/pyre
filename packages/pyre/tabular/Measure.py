# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..records.Field import Field


class Measure(Field):
    """
    The base class for table descriptors
    """


    # public data in addition to what is inherited from Field
    index = False # True when this measure is a primary key that can be used to create an index


# end of file 
