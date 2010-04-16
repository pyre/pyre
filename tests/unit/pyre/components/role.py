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
    from pyre.components.Role import Role
    from pyre.components.Trait import Trait

    # declare a class
    class configurable(Configurable, metaclass=Role):
        """test class"""

        # declare some traits
        trait1 = Trait()
        trait2 = Trait()

    # now verify that attribute classification worked as expected
    assert configurable._pyre_category == None
    # did the _pyre_Inventory embedded class get built?
    assert hasattr(configurable, "_pyre_Inventory")
    # get the trait categories
    categories = configurable._pyre_Inventory._pyre_categories
    # chec the traits are there
    assert categories["traits"] == ( configurable.trait1, configurable.trait2 )
        
    return


# main
if __name__ == "__main__":
    test()


# end of file 
