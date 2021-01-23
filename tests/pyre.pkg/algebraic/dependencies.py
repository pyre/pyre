#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Verify that we can traverse the expression tree correctly and completely
    """

    # access to the basic node
    import pyre.algebraic

    # N.B. the assertions in this test must be done more carefully if nodes have {ordering}
    # since then the equality test becomes a node. the implementation of {node} below does not
    # include {ordering}, so we should be ok with naive checks.

    # declare a node class
    class node(metaclass=pyre.algebraic.algebra, basenode=True):
        """
        The base node
        """

        class literal:
            """
            An implementation of literals
            """
            # public data
            value = None
            # metamethods
            def __init__(self, value, **kwds):
                # chain up
                super().__init__(**kwds)
                # save the value
                self.value = value
                # all done
                return


    # declare a couple of nodes
    n1 = node.variable()
    n2 = node.variable()

    # check that they have no dependencies
    assert list(n1.literals) == []
    assert list(n2.literals) == []
    assert list(n1.operators) == []
    assert list(n2.operators) == []
    assert list(n1.variables) == [ n1 ]
    assert list(n2.variables) == [ n2 ]

    # an expression involving a unary operator
    n = -n1
    assert list(n.operators) == [ n ]
    assert list(n.variables) == [ n1 ]

    # an expression involving a literal
    n = 2*n1
    assert list(n.operators) == [ n ]
    assert list(n.variables) == [ n1 ]

    # an expression involving a binary operator
    n = n1 + n2
    assert list(n.operators) == [ n ]
    assert list(n.variables) == [ n1,  n2 ]

    # add another layer
    m = n + n
    assert list(m.variables) == [ n1,  n2 ] * 2
    assert list(m.operators) == [ m,  n, n ]
    # and one more
    l = m + m
    assert list(l.variables) == [ n1,  n2 ] * 4
    assert list(l.operators) == [ l,  m,  n,  n,  m,  n,  n ]

    # a more complicated example
    assert set((2*(.5 - n1*n2 + n2**2)*n1).variables) == { n1,  n2 }

    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
