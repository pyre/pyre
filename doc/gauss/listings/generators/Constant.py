# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from Functor import Functor


class Constant(Functor):
    """
    A representation of the unit function
    """

    # interface
    def eval(self, points):
        """
        Compute the value of the function: return 1
        """
        constant = self.constant
        for point in points:
            yield constant
        return

    # meta methods
    def __init__(self, constant):
        self.constant = constant
        return


# end of file 
