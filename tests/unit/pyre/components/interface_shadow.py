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
        common.default = "base"

    # and derive another from it
    class derived(base):
        """a derived interface"""
        # traits
        common = Property()
        common.default = "derived"
        
    # check that everything is as expected with base
    assert base._pyre_configurables == (base, Interface)
    # access the traits of base
    assert base.common._pyre_category == "properties"
    assert base.common.default == "base"
     
    # check that everything is as expected with derived
    assert derived._pyre_configurables == (derived, base, Interface)
    # access the traits of derived
    assert derived.common._pyre_category == "properties"
    assert derived.common.default == "derived"

    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
