# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Variable:
    """
    Mix-in class to encapsulate nodes 
    """


    # constants
    category = 'variable'


    # support for graph traversals
    def identify(self, authority, **kwds):
        """Let {authority} know I am a variable"""
        # invoke the callback
        return authority.onVariable(descriptor=self, **kwds)


# end of file 
