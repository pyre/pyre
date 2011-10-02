#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that node substitution respects the expression graph invariants
"""


def test():
    # get the package
    import pyre.calc
    # build some nodes
    n1 = pyre.calc.var()
    n2 = pyre.calc.var()
    n3 = pyre.calc.var()

    # first, something simple
    s = n1 + n2

    # we expect:
    # n1 to have one observer: s
    assert len(n1.observers) == 1
    assert identical((ref() for ref in n1.observers), [s])
    # n2 to have one observer: s
    assert len(n2.observers) == 1
    assert identical((ref() for ref in n2.observers), [s])
    # n3 to have no observers
    assert len(n3.observers) == 0
    # s to have two operands: n1 and n2
    assert len(s.operands) == 2
    assert identical(set(s.operands), {n1, n2})
    # and no observers
    assert len(s.observers) == 0
    
    # make a substitution
    s.pyre_substitute(current=n1, replacement=n3)
    # we expect:
    # n1 to have no observers
    assert len(n1.observers) == 0
    # n2 to have one observer: s
    assert len(n2.observers) == 1
    assert identical((ref() for ref in n2.observers), [s])
    # n3 to have one observer: s
    assert len(n3.observers) == 1
    assert identical((ref() for ref in n3.observers), [s])
    # s to have two operands: n2 and n3
    assert len(s.operands) == 2
    assert identical(set(s.operands), {n2, n3})
    # and no observers
    assert len(s.observers) == 0

    # attempt to create a cycle
    try:
        s.pyre_substitute(current=n3, replacement=s)
        assert False
    except s.CircularReferenceError:
        pass

    return


def identical(s1, s2):
    """
    Verify that the nodes in {s1} and {s2} are identical. This has to be done carefully since
    we must avoid triggering __eq__
    """
    # for the pairs
    for n1, n2 in zip(s1, s2):
        # check them for _identity_, not _equality_
        if n1 is not n2: return False
    # all done
    return True
            

# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
