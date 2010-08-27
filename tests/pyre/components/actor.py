#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the Actor metaclass decorates class records properly
"""


def test():
    # access
    from pyre.components.Component import Component

    # declare a class
    class base(Component):
        """test class"""

    # did my ancestor list get built properly
    assert base.pyre_pedigree == (base, Component)
        
    return base


# main
if __name__ == "__main__":
    test()


# end of file 
