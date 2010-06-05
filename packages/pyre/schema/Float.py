# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Type import Type


class Float(Type):
    """
    A floating point type declarator
    """


    # interface
    @classmethod
    def cast(cls, value):
        """
        Attempt to convert {value} into a float
        """
        try:
            return float(value)
        except TypeError as error:
            raise cls.CastingError(msg=str(error)) from error
        except ValueError as error:
            raise cls.CastingError(msg=str(error)) from error


    # exception
    from . import CastingError


# end of file 
