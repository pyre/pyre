# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import units
# my superclass
from .Type import Type


# declaration
class Dimensional(Type):
    """
    A type declarator for quantities with units
    """


    # constants
    typename = 'dimensional' # the name of my type
    default = units.zero # my default value


    # public data
    parser = units.parser()


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Attempt to convert {value} into a dimensional
        """
        # use the unit parser to convert strings to dimensionals 
        if isinstance(value, str): return cls.parser.parse(value)
        # dimensionals go right through
        if isinstance(value, units.dimensional): return value
        # everything else is an error
        msg="could not convert {0.value!r} into a dimensional quantity"
        raise cls.CastingError(value=value, description=msg)
        

    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
