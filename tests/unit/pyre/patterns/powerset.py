#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that powerset works
"""


def test():
    import pyre.patterns

    l = [1,2,3]

    p = list(pyre.patterns.powerset(l))
    answer = [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]

    assert p == answer

    return p


# main
if __name__ == "__main__":
    test()


# end of file 
