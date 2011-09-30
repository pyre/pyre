# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Literal:
    """
    Class that encapsulates values encountered in expressions that are not instance of members
    of the {Node} class hierarchy.
    """


    # public data
    span = [] # literals are not proper nodes
    variables = [] # literals are not variables and have no dependencies
    operators = [] # literals are not operators and have no dependencies


    # interface
    def getValue(self):
        """
        Return my value
        """
        return self._value


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
        self._value = value
        return


    # private data
    _value = None


# end of file 
