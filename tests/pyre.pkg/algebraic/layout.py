#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Verify the node layout
    """

    # access the package
    import pyre.algebraic

    # the algebra
    algebra = pyre.algebraic.algebra

    # declare a node class
    class node(metaclass=algebra, basenode=True, arithmetic=True, boolean=True, ordering=True):
        """
        The base node class
        """

    # verify that the {mro} is what we expect
    assert node.__mro__ == (
        node,
        algebra.base,
        algebra.arithmetic, algebra.ordering, algebra.boolean,
        object)

    # check literals
    assert node.literal.__mro__ == (
        node.literal, algebra.literal, algebra.leaf,
        node,
        algebra.base,
        algebra.arithmetic, algebra.ordering, algebra.boolean,
        object)

    # check variables
    assert node.variable.__mro__ == (
        node.variable, algebra.variable, algebra.leaf,
        node,
        algebra.base,
        algebra.arithmetic, algebra.ordering, algebra.boolean,
        object)

    # check operator
    assert node.operator.__mro__ == (
        node.operator, algebra.operator, algebra.composite,
        node,
        algebra.base,
        algebra.arithmetic, algebra.ordering, algebra.boolean,
        object)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
