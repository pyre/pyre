# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
from .. import units
# my superclass
from .Numeric import Numeric


# declaration
class Dimensional(Numeric):
    """
    A type declarator for quantities with units
    """


    # constants
    typename = 'dimensional' # the name of my type


    # public data
    parser = units.parser()


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a dimensional
        """
        # use the unit parser to convert strings to dimensionals 
        if isinstance(value, str): return self.parser.parse(value)
        # dimensionals go right through
        if isinstance(value, units.dimensional): return value
        # everything else is an error
        msg="could not convert {0.value!r} into a dimensional quantity"
        raise self.CastingError(value=value, description=msg)
        

    # meta-methods
    def __init__(self, default=units.zero, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
