# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Entry import Entry


class Literal(Entry):
    """
    Class that encapsulates values encountered in expressions that are not instance of members
    of the {Entry} class hierarchy.
    """


    # types
    from ..calc.Literal import Literal as node


    # public data
    value = None # my value is explicitly set
    variables = [] # literals are not variables and have no dependencies
    operators = [] # literals are not operators and have no dependencies


    # interface
    def buildNode(self, stream, model):
        """
        Extract a value from {stream} and use it to build a {pyre.calc} node 
        """
        # easy enough
        return self.node(value=self.value)


    def evaluate(self, stream, cache):
        """
        Compute my value by either returning the encapsulated constant 
        """
        # easy enough...
        return self.value

        
    def substitute(self, current, replacement):
        """
        Traverse my expression graph and replace all occurrences of node {current} with
        {replacement}
        """
        # nothing to do
        return


    # meta methods
    def __init__(self, value, **kwds):
        super().__init__(**kwds)
        self.value = value
        return


# end of file 
