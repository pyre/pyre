#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


"""
Verify that we can traverse the expression tree correctly and completely
"""


def test():

    # access to the basic node
    import pyre.algebraic

    # declare a node class
    class node(metaclass=pyre.algebraic.algebra): pass

    # declare a couple of nodes
    n1 = node.variable()
    n2 = node.variable()

    # check that they have no dependencies
    assert tuple(id(v) for v in n1.variables) == (id(n1),)
    assert tuple(id(v) for v in n2.variables) == (id(n2),)
    assert tuple(id(v) for v in n1.operators) == ()
    assert tuple(id(v) for v in n2.operators) == ()

    # an expression involving a unary operator
    n = -n1
    assert tuple(id(v) for v in n.variables) == (id(n1),)
    assert tuple(id(o) for o in n.operators) == (id(n),)

    # an expression involving a literal
    n = 2*n1
    assert tuple(id(v) for v in n.variables) == (id(n1),)
    assert tuple(id(v) for v in n.operators) == (id(n),)

    # an expression involving a binary operator
    n = n1 + n2
    assert tuple(id(v) for v in n.variables) == (id(n1), id(n2))
    assert tuple(id(v) for v in n.operators) == (id(n),)

    # add another layer
    m = n + n
    assert tuple(id(v) for v in n.variables) == (id(n1), id(n2))
    assert tuple(id(v) for v in m.operators) == (id(m), id(n) ,id(n))
    # and one more
    l = m + m
    assert set(id(v) for v in l.variables) == {id(n1), id(n2)}
    assert tuple(id(v) for v in l.operators) == (id(l), id(m), id(n), id(n), id(m), id(n), id(n))

    # a more complicated example
    assert set(id(v) for v in (2*(.5 - n1*n2 + n2**2)*n1).variables) == {id(n1), id(n2)}

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
