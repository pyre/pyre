# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


class Literal:
    """
    Class that encapsulates values encountered in expressions that are not instances of members
    of the {Node} class hierarchy.
    """


    # constants
    category = 'literal'


    # interface
    @property
    def literals(self):
        """
        Return a sequence of the literals in my span
        """
        # i am one
        yield self
        # and nothing further
        return


    # support for graph traversals
    def identify(self, authority, **kwds):
        """
        Let {authority} know I am a literal
        """
        # invoke the callback
        return authority.onLiteral(literal=self, **kwds)


# end of file
