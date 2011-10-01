# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..algebraic.Literal import Literal as Base


class Literal(Base):
    """
    Class that encapsulates values encountered in expressions that are not instance of members
    of the {Node} class hierarchy.
    """

    # public data
    observers = ()

    
    @property
    def value(self):
        return self._value


    # interface
    def addObserver(self, *args, **kwds):
        """
        Stub for the observable interface
        """
        return


    def removeObserver(self, *args, **kwds):
        """
        Stub for the observable interface
        """
        return


# end of file 
