#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Exercise the {named} pattern
"""

  
def test():
    from pyre.patterns.Named import Named

    class named(Named):
        """
        Trivial class to enable testing Named
        """

    n = named(name="test")
    assert n.name == "test"

    return n


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
