#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise interface inheritance
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
        extra = Property()
        
    # check that everything is as expected with base
    assert base._pyre_configurables == (base, Interface)
    # access the traits of base
    assert base.pyre_getTraitDescriptor("common")._pyre_category == "properties"
    # make sure derivation did not cause any pollution
    assert base.pyre_getTraitDescriptor("extra") == None
     
    # check that everything is as expected with derived
    assert derived._pyre_configurables == (derived, base, Interface)
    # access the traits of derived
    assert derived.pyre_getTraitDescriptor("common")._pyre_category == "properties"
    assert derived.pyre_getTraitDescriptor("extra")._pyre_category == "properties"

    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
