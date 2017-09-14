# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


class Variable:
    """
    Mix-in class to encapsulate nodes
    """


    # constants
    category = 'variable'


    # support for graph traversals
    def identify(self, authority, **kwds):
        """
        Let {authority} know I am a variable
        """
        # invoke the callback
        return authority.onVariable(variable=self, **kwds)


# end of file
