#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that traits are shadowed properly in the presence of inheritance
"""


def test():
    # access
    from pyre.components.Property import Property
    from pyre.components.Component import Component

    # declare an component
    class base(Component):
        """a base component"""
        # traits
        common = Property()
        common.default = "base"

    # and derive another from it
    class derived(base):
        """a derived component"""
        # traits
        common = Property()
        common.default = "derived"
        
    # get the trait descriptors
    base_common = base.pyre_getTraitDescriptor("common")
    derived_common = derived.pyre_getTraitDescriptor("common")
    # verify the traits were shadowed properly
    assert base_common is not derived_common
    assert base.common == "base"
    assert derived.common == "derived"
     
    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
