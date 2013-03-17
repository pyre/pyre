# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access the type declarators
from .. import schemata
# the base class
from .Measure import Measure


# convenience factories that build measures of specific types
class dimensional(Measure):
    """
    Build a measure that has units

    Legal assignments are constrained to have units compatible with the default value
    """

    default = 0
    schema = schemata.dimensional

    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


class float(Measure):
    """
    Build a float measure
    """

    default = 0
    schema = schemata.float

    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


class int(Measure):
    """
    Build an integer measure
    """

    default = 1
    schema = schemata.int

    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


class str(Measure):
    """
    Build a string measure
    """

    default = ""
    schema = schemata.str

    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
