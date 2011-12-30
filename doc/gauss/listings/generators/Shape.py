# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Shape(object):
    """
    The abstract base class for representations of geometrical regions
    """

    # interface
    def interior(self, points):
        """
        Predicate that checks whether {point} falls on my interior
        """
        raise NotImplementedError(
            "class {.__name__!r} should implement 'interior'".format(type(self)))


# end of file 
