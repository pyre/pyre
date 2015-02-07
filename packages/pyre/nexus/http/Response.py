# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import collections # for ordered dict


# class declaration
class Response:
    """
    Encapsulation of the response to an http client request
    """


    # public data
    meta = None # an ordered dictionary of meta information about the document


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the header storage
        self.meta = collections.OrderedDict()
        # all done
        return


# end of file
