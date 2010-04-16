#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the Requirement metaclass decorates class records properly
"""


def test():
    # access
    from pyre.components.Configurable import Configurable
    from pyre.components.Requirement import Requirement
    from pyre.components.Trait import Trait

    # declare a class
    class base(object, metaclass=Requirement, family="generic"):
        """test class"""
        
    return


# main
if __name__ == "__main__":
    test()


# end of file 
