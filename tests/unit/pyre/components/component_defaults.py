#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify trait access through the component class attributes
"""


def test():
    # access
    import pyre.components
    from pyre.components.Component import Component
    from pyre.components.Property import Property

    # declare a component hierarchy
    class base(Component):
        """the base component"""
        # traits
        common = Property()
        common.default = "base"

        a1 = Property()
        a1.default = "base"

        a2 = Property()
        a2.default = "base"

        @pyre.components.export
        def do(self):
            """behave"""
            return "base"

    class a1(base):
        """an intermediate"""
        # traits
        a1 = Property()
        a1.default = "a1"

    class a2(base):
        """another intermediate"""
        # traits
        a2 = Property()
        a2.default = "a2"

    class derived(a1, a2):
        """a derived component"""
        common = Property()
        common.default = "derived"

        extra = Property()
        extra.default = "derived"

        @pyre.components.export
        def do(self):
            """behave"""
            return "derived"

    # check base
    inventory = base._pyre_Inventory
    assert inventory.common.value == "base"
    assert inventory.a1.value == "base"
    assert inventory.a2.value == "base"

    # check a1
    inventory = a1._pyre_Inventory
    assert inventory.common.value == "base"
    assert inventory.a1.value == "a1"
    assert inventory.a2.value == "base"

    # check a2
    inventory = a2._pyre_Inventory
    assert inventory.common.value == "base"
    assert inventory.a1.value == "base"
    assert inventory.a2.value == "a2"

    # check derived
    inventory = derived._pyre_Inventory
    assert inventory.common.value == "derived"
    assert inventory.a1.value == "a1"
    assert inventory.a2.value == "a2"
    assert inventory.extra.value == "derived"

    # now set the derived default of a1
    derived._pyre_Inventory.a1.value = "derived"
    # check that the assignmenttook place
    assert derived._pyre_Inventory.a1.value == "derived"
    # and check that a1 is unaltered
    assert a1._pyre_Inventory.a1.value == "a1"
    
    return base, a1, a2, derived
     

# main
if __name__ == "__main__":
    test()


# end of file 
