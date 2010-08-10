#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise multiple inheritance among components
"""


def test():
    # access
    import pyre.components
    from pyre.components.Component import Component
    from pyre.components.Property import Property

    # declare an component hierarchy
    class base(Component):
        # traits
        common = Property()
        common.default = "base"

        a1 = Property()
        a1.default = "base"

        a2 = Property()
        a2.default = "base"

    class a1(base):
        # traits
        a1 = Property()
        a1.default = "a1"

    class a2(base):
        # traits
        a2 = Property()
        a2.default = "a2"

    class derived(a1, a2):
        """a derived component"""
        common = Property()
        common.default = "derived"

        extra = Property()
        extra.default = "derived"
        
    # check that everything is as expected with the hierachy
    assert base._pyre_configurables == (base, Component)
    assert a1._pyre_configurables == (a1, base, Component)
    assert a2._pyre_configurables == (a2, base, Component)
    assert derived._pyre_configurables == (derived, a1, a2, base, Component)

    # check the _pyre_Inventory constructions
    # first the expected inheritance relations
    assert issubclass(base._pyre_Inventory, Component._pyre_Inventory)
    assert issubclass(a1._pyre_Inventory, base._pyre_Inventory)
    assert issubclass(a1._pyre_Inventory, Component._pyre_Inventory)
    assert issubclass(a2._pyre_Inventory, base._pyre_Inventory)
    assert issubclass(a2._pyre_Inventory, Component._pyre_Inventory)
    assert issubclass(derived._pyre_Inventory, a1._pyre_Inventory)
    assert issubclass(derived._pyre_Inventory, a2._pyre_Inventory)
    assert issubclass(derived._pyre_Inventory, base._pyre_Inventory)
    assert issubclass(derived._pyre_Inventory, Component._pyre_Inventory)
    # and, more thoroughly, the __mro__
    assert base._pyre_Inventory.__mro__ == (
        base._pyre_Inventory,
        Component._pyre_Inventory, object)
    assert a1._pyre_Inventory.__mro__ == (
        a1._pyre_Inventory, base._pyre_Inventory,
        Component._pyre_Inventory, object)
    assert a2._pyre_Inventory.__mro__ == (
        a2._pyre_Inventory, base._pyre_Inventory,
        Component._pyre_Inventory, object)
    assert derived._pyre_Inventory.__mro__ == (
        derived._pyre_Inventory, a1._pyre_Inventory, a2._pyre_Inventory, base._pyre_Inventory,
        Component._pyre_Inventory, object)

    # access the traits of base
    assert base.common == "base"
    assert base.a1 == "base"
    assert base.a2 == "base"
    # access the traits of a1
    assert a1.common == "base"
    assert a1.a1 == "a1"
    assert a1.a2 == "base"
    # access the traits of a2
    assert a2.common == "base"
    assert a2.a1 == "base"
    assert a2.a2 == "a2"
    # access the traits of derived
    assert derived.common == "derived"
    assert derived.a1 == "a1"
    assert derived.a2 == "a2"
    assert derived.extra == "derived"

    # make sure derivation did not cause any pollution
    try:
        base.extra
        assert False
    except AttributeError:
        pass

    return base, a1, a2, derived
     

# main
if __name__ == "__main__":
    test()


# end of file 
