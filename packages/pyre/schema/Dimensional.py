# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Type import Type
from ..units import parser as parserFactory
from ..units.Dimensional import Dimensional


class Dimensional(Type):
    """
    A type declarator for quantities with dimensions
    """


    # interface
    @classmethod
    def cast(cls, value):
        """
        Attempt to convert {value} into a dimensional
        """
        # use the unit parser to convert strings to dimensionals 
        if isinstance(value, str):
            return cls.parser.parse(value)
        # dimensionals go right through
        if isinstance(value, Dimensional):
            return value
        # everything else is an error
        msg="could not convert {!r} into a dimensional quantity".format(value)
        raise cls.CastingError(value=value, msg=msg)
        

    # public data
    parser = parserFactory()


# end of file 
