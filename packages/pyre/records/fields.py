# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access to the type specifiers
from .. import schemata
# base class
from .Entry import Entry.variable as field


# typed field declarators
class float(field):
    """
    A floating point field
    """

    default = 0
    schema = schemata.float

    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


class int(field):
    """
    An integer field
    """

    default = 0
    schema = schemata.int

    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


class str(field):
    """
    A string field
    """

    default = ""
    schema = schemata.str

    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
