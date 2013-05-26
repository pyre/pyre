# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Literal:
    """
    Class that encapsulates values encountered in expressions that are not instances of members
    of the {Node} class hierarchy.
    """


    # constants
    category = 'literal'


    # public data
    span = () # literals are not proper nodes so their span is empty
    operands = () # literals have no operands
    variables = () # empty span
    operators = () # empty span


    # graph traversal
    def unique(self, encountered=None):
        """
        Traverse my expression graph and visit all nodes not previously {encountered}
        """
        # if I have been visited before, nothing left to do
        if self in encountered: return
        # otherwise, add me to the pile
        encountered.add(self)
        # announce
        yield self
        
        # all done
        return
        

# end of file 
