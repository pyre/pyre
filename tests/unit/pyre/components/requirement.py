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
    class base(Configurable, metaclass=Requirement, family="generic"):
        """test class"""

        # declare some traits
        trait1 = Trait()
        trait2 = Trait()

    # now verify that attribute classification worked as expected
    assert base._pyre_family == "generic"
    assert base._pyre_category == None
    # did the _pyre_Inventory embedded class get built?
    assert hasattr(base, "_pyre_Inventory")
    # get the trait categories
    categories = base._pyre_Inventory._pyre_categories
    # chec the traits are there
    assert categories["traits"] == ( base.trait1, base.trait2 )
        
    return


# main
if __name__ == "__main__":
    test()


# end of file 
