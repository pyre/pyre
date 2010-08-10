#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise multiple inheritance among interfaces
"""


def test():
    # access
    import pyre.components
    from pyre.components.Interface import Interface
    from pyre.components.Property import Property

    # declare an interface hierarchy
    class base(Interface):
        # traits
        common = Property()
        a1 = Property()
        a2 = Property()

    class a1(base):
        # traits
        a1 = Property()

    class a2(base):
        # traits
        a2 = Property()

    class derived(a1, a2):
        """a derived interface"""
        common = Property()
        extra = Property()
        
    # check that everything is as expected with the hierachy
    assert base._pyre_configurables == (base, Interface)
    assert a1._pyre_configurables == (a1, base, Interface)
    assert a2._pyre_configurables == (a2, base, Interface)
    assert derived._pyre_configurables == (derived, a1, a2, base, Interface)

    # check the _pyre_Inventory constructions
    # first the expected inheritance relations
    assert issubclass(base._pyre_Inventory, Interface._pyre_Inventory)
    assert issubclass(a1._pyre_Inventory, base._pyre_Inventory)
    assert issubclass(a1._pyre_Inventory, Interface._pyre_Inventory)
    assert issubclass(a2._pyre_Inventory, base._pyre_Inventory)
    assert issubclass(a2._pyre_Inventory, Interface._pyre_Inventory)
    assert issubclass(derived._pyre_Inventory, a1._pyre_Inventory)
    assert issubclass(derived._pyre_Inventory, a2._pyre_Inventory)
    assert issubclass(derived._pyre_Inventory, base._pyre_Inventory)
    assert issubclass(derived._pyre_Inventory, Interface._pyre_Inventory)
    # and, more thoroughly, the __mro__
    assert base._pyre_Inventory.__mro__ == (
        base._pyre_Inventory,
        Interface._pyre_Inventory, object)
    assert a1._pyre_Inventory.__mro__ == (
        a1._pyre_Inventory, base._pyre_Inventory,
        Interface._pyre_Inventory, object)
    assert a2._pyre_Inventory.__mro__ == (
        a2._pyre_Inventory, base._pyre_Inventory,
        Interface._pyre_Inventory, object)
    assert derived._pyre_Inventory.__mro__ == (
        derived._pyre_Inventory, a1._pyre_Inventory, a2._pyre_Inventory, base._pyre_Inventory,
        Interface._pyre_Inventory, object)

    # access the traits of base
    base_common = base.pyre_getTraitDescriptor("common")
    base_a1 = base.pyre_getTraitDescriptor("a1")
    base_a2 = base.pyre_getTraitDescriptor("a2")
    # access the traits of a1
    a1_common = a1.pyre_getTraitDescriptor("common")
    a1_a1 = a1.pyre_getTraitDescriptor("a1")
    a1_a2 = a1.pyre_getTraitDescriptor("a2")
    # access the traits of a2
    a2_common = a2.pyre_getTraitDescriptor("common")
    a2_a1 = a2.pyre_getTraitDescriptor("a1")
    a2_a2 = a2.pyre_getTraitDescriptor("a2")
    # access the traits of derived
    derived_common = derived.pyre_getTraitDescriptor("common")
    derived_a1 = derived.pyre_getTraitDescriptor("a1")
    derived_a2 = derived.pyre_getTraitDescriptor("a2")
    derived_extra = derived.pyre_getTraitDescriptor("extra")

    # verify the expected relationships
    # a1
    assert a1_common is base_common
    assert a1_a1 is not base_a1
    assert a1_a2 is base_a2
    # a2
    assert a2_common is base_common
    assert a2_a1 is base_a1
    assert a2_a2 is not base_a2
    # derived
    assert derived_common is not base_common
    assert derived_a1 is not base_a1
    assert derived_a1 is a1_a1
    assert derived_a2 is not base_a2
    assert derived_a2 is a2_a2

    # all done
    return base, a1, a2, derived
     

# main
if __name__ == "__main__":
    test()


# end of file 
