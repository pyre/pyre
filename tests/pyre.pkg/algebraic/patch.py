#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Verify that we can successfully perform surgery in an expression tree
    """

    # access to the package
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
    n3 = node.variable()

    # check that they have no dependencies
    assert list(n1.variables) == [ n1 ]
    assert list(n2.variables) == [ n2 ]
    assert list(n3.variables) == [ n3 ]

    # a simple expression
    n = n1 + n2
    assert list(n.variables) == [ n1,  n2 ]
    # patch {n3} in
    n.substitute(current=n1, replacement=n3)
    # and check that it happened correctly
    assert list(n.variables) == [ n3,  n2 ]

    # add another layer
    m = n1 + n2 + n3
    assert list(m.variables) == [ n1,  n2,  n3 ]
    # patch {n} in
    m.substitute(current=n3, replacement=n)
    # check
    assert list(m.variables) == [ n1,  n2,  n3,  n2 ]

    # a more complicated example
    n = (2*(n1**2 - 2*n1*n2 + n2**2)*n3)
    assert set(n.variables) == { n1,  n2,  n3 }
    # patch {n3} in
    n.substitute(current=n1, replacement=n3)
    # and check that it happened correctly
    assert set(n.variables) == { n2,  n3 }

    # let's try
    try:
        # to make a cycle
        n.substitute(current=n2, replacement=n)
        # which should fail
        assert False, "unreachable"
    # catch it
    except n.CircularReferenceError:
        # all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
