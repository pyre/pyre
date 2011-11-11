# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Shape(object):
    """
    The abstract base class for representations of geometrical regions
    """


    # interface
    def interior(self, points):
        """
        Examine each point in {points} and return a list of booleans indicating whether it is
        interior or not
        """
        raise NotImplementedError(
            "class {.__name__!r} should implement 'interior'".format(type(self)))


# end of file 
