#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Explore the implementations of container membership operations in the presence of an
    overloaded {__eq__}
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

    # declare a couple of nodes
    v1 = node.variable()
    v2 = node.variable()

    # tuples are affected
    t = (v1,)
    # both {v1} and {v2} are reported as members because of the overloaded {__eq__}
    assert v1 in t
    assert v2 in t
    # the correct way to test membership looks like this: loop over the container
    for v in t:
        # and use {is} which does not invoke {__eq__}
        assert v is not v2

    # lists are affected
    l = [v1]
    # both {v1} and {v2} are reported as members because of the overloaded {__eq__}
    assert v1 in l
    assert v2 in l
    # the correct way to test membership looks like this: loop over the container
    for v in l:
        # and use {is} which does not invoke {__eq__}
        assert v is not v2

    # sets are not affected
    s = {v1}
    # {v1} is reported as a member of the set; {v2} is not
    assert v1 in s
    assert v2 not in s

    # dictionaries are not affected
    d = {v1: None}
    # {v1} is reported as a member of the dictionary; {v2} is not
    assert v1 in d
    assert v2 not in d
    # {v1} is reported among the keys; {v2} is not
    assert v1 in d.keys()
    assert v2 not in d.keys()

    # generators are affected
    def g():
        yield v1
        return

    # both {v1} and {v2} are reported as members because of the overloaded {__eq__}
    assert v1 in g()
    assert v2 in g()
    # a good way to test membership is to realize as a set
    assert v1 in set(g())
    assert v2 not in set(g())

    # all done
    return node


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
