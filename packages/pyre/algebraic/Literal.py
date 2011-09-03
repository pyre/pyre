# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Literal(Node):
    """
    Class that encapsulates values encountered in expressions that are not instance of members
    of the {Node} class hierarchy.
    """


    # public data
    value = None # my value is explicitly set
    variables = [] # literals have no dependencies


    # interface
    def substitute(self, replacements):
        """
        Replace variables in my graph that are present in {replacements} with the indicated node
        """
        # nothing to do
        return


    # meta methods
    def __init__(self, value, **kwds):
        super().__init__(**kwds)
        self.value = value
        return


# end of file 
