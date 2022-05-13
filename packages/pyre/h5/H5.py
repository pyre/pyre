#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# superclass
from .Group import Group


# a dataset container
class H5(Group):
    """
    An h5 file
    """


    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # all done
        return


# end of file
