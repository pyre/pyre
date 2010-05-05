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
    from pyre.components.Interface import Interface

    # declare an interface
    class base(Interface):
        """a base interface"""
        # traits
        common = Property()

    # and derive another from it
    class derived(base):
        """a derived interface"""
        # traits
        common = Property()
        
    # check that everything is as expected with base
    assert base._pyre_configurables == (base, Interface)
    # access the traits of base
    base_common = base.pyre_getTraitDescriptor("common")
    assert base_common._pyre_category == "properties"
     
    # check that everything is as expected with derived
    assert derived._pyre_configurables == (derived, base, Interface)
    # access the traits of derived
    derived_common = derived.pyre_getTraitDescriptor("common")
    assert derived_common._pyre_category == "properties"

    # make sure that the two descriptors are unrelated
    assert base_common is not derived_common

    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
