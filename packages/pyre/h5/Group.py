#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2022 all rights reserved
#


# metaclass
from .Schema import Schema


# a dataset container
class Group(metaclass=Schema):
    """
    A container of datasets
    """


    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # all done
        return


# end of file
