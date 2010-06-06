# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Type import Type


class Object(Type):
    """
    A type declarator for generic python objects
    """


    # interface
    @classmethod
    def cast(cls, value):
        """
        Convert {value} into a python object; this is trivial for me
        """
        return value


# end of file 
