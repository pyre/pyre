#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


"""
Exercise node algebra
"""


def test():
    # access the various operator
    import operator
    # access the package
    import pyre.algebraic

    # declare a node class
    class node(metaclass=pyre.algebraic.algebra): pass

    # declare a couple of nodes
    n1 = node.variable()
    n2 = node.variable()

    # check
    check_binary(n1 & n2, operator.and_, n1, n2)
    check_binary(n1 | n2, operator.or_, n1, n2)

    check_right(n1 & 2, operator.and_, 2, n1)
    check_right(n1 | 2, operator.or_, 2, n1)

    check_left(1 & n2, operator.and_, 1, n2)
    check_left(1 | n2, operator.or_, 1, n2)

    return node


# the checkers
def check_binary(expression, operator, op1, op2):
    assert expression.evaluator is operator
    assert expression.operands[0] is op1
    assert expression.operands[1] is op2
    return


def check_left(expression, operator, value, node):
    assert expression.evaluator is operator
    assert expression.operands[0].value == value
    assert expression.operands[1] is node
    return


def check_right(expression, operator, value, node):
    assert expression.evaluator is operator
    assert expression.operands[0] is node
    assert expression.operands[1].value == value
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
