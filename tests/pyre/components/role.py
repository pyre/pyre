#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the Role metaclass decorates class records properly
"""


def test():
    # access
    from pyre.components.Configurable import Configurable
    from pyre.components.Role import Role

    # declare a class
    class base(Configurable, metaclass=Role):
        """test class"""

    # did my ancestor list get built properly
    assert base.pyre_pedigree == [base]
        
    return base


# main
if __name__ == "__main__":
    test()


# end of file 
