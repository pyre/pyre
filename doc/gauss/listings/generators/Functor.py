# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Functor(object):
    """
    The abstract base class for function objects
    """

    # interface
    def eval(self, points):
        """
        Evaluate the function at the supplied points
        """
        raise NotImplementedError(
            "class {.__name__!r} should implement 'eval'".format(type(self)))


# end of file 
