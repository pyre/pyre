#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise the ordering operations among nodes
    """

    # access the various operator
    import operator
    # access the package
    import pyre.algebraic

    # declare a node class
    class node(metaclass=pyre.algebraic.algebra, basenode=True, arithmetic=False, ordering=True):
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

    # check some expressions among nodes
    check_binary(n1 == n2, operator.eq, n1, n2)
    check_binary(n1 <= n2, operator.le, n1, n2)
    check_binary(n1 < n2, operator.lt, n1, n2)
    check_binary(n1 >= n2, operator.ge, n1, n2)
    check_binary(n1 > n2, operator.gt, n1, n2)
    check_binary(n1 != n2, operator.ne, n1, n2)

    # expressions between nodes and literals
    check_literal(n1 == 2, operator.eq, n1, 2)
    check_literal(n1 <= 2, operator.le, n1, 2)
    check_literal(n1 < 2, operator.lt, n1, 2)
    check_literal(n1 >= 2, operator.ge, n1, 2)
    check_literal(n1 > 2, operator.gt, n1, 2)
    check_literal(n1 != 2, operator.ne, n1, 2)

    # expressions between literals and nodes
    # {eq} and {ne} are their own reflections
    check_literal(1 == n2, operator.eq, n2, 1)
    check_literal(1 != n2, operator.ne, n2, 1)
    # {lt} and {gt} are each other's reflections
    check_literal(1 < n2, operator.gt, n2, 1)
    check_literal(1 > n2, operator.lt, n2, 1)
    # {le} and {ge} are each other's reflections
    check_literal(1 <= n2, operator.ge, n2, 1)
    check_literal(1 >= n2, operator.le, n2, 1)

    # all done
    return node


# the checkers
def check_binary(expression, operator, op1, op2):
    assert expression.evaluator is operator
    assert expression._operands[0] is op1
    assert expression._operands[1] is op2
    return

def check_literal(expression, operator, op, literal):
    assert expression.evaluator is operator
    assert expression._operands[0] is op
    assert [ l.value for l in expression.literals] == [ literal ]
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
