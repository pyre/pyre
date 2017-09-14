# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
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
    variables = () # and so is their list of nodes

    # literals get a value accessor regardless of whether the rest of the algebra supports
    # value access
    @property
    def value(self):
        """
        Value accessor
        """
        return self._value


    # meta-methods
    def __init__(self, value, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the foreign object as my value
        self._value = value
        # all done
        return


    # support for graph traversals
    def identify(self, authority, **kwds):
        """
        Let {authority} know I am a literal
        """
        # invoke the callback
        return authority.onLiteral(literal=self, **kwds)


# end of file
