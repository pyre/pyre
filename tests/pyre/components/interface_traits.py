#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that trait access using pyre_traits works as expected
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

        @pyre.components.export
        def do(self):
            """behave"""

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

        @pyre.components.export
        def do(self):
            """behave"""

    # access the traits of base
    base_common = base.pyre_getTraitDescriptor("common")
    base_a1 = base.pyre_getTraitDescriptor("a1")
    base_a2 = base.pyre_getTraitDescriptor("a2")
    base_do = base.pyre_getTraitDescriptor("do")
    # access the traits of a1
    a1_common = a1.pyre_getTraitDescriptor("common")
    a1_a1 = a1.pyre_getTraitDescriptor("a1")
    a1_a2 = a1.pyre_getTraitDescriptor("a2")
    a1_do = base.pyre_getTraitDescriptor("do")
    # access the traits of a2
    a2_common = a2.pyre_getTraitDescriptor("common")
    a2_a1 = a2.pyre_getTraitDescriptor("a1")
    a2_a2 = a2.pyre_getTraitDescriptor("a2")
    a2_do = base.pyre_getTraitDescriptor("do")
    # access the traits of derived
    derived_common = derived.pyre_getTraitDescriptor("common")
    derived_a1 = derived.pyre_getTraitDescriptor("a1")
    derived_a2 = derived.pyre_getTraitDescriptor("a2")
    derived_extra = derived.pyre_getTraitDescriptor("extra")
    derived_do = derived.pyre_getTraitDescriptor("do")

    # check base
    traits = [trait for trait,cls in base.pyre_traits()]
    assert traits == [base_common, base_a1, base_a2, base_do]
    traits = [trait for trait,cls in base.pyre_traits(categories=['behaviors'])]
    assert traits == [base_do]
    traits = [trait for trait,cls in base.pyre_traits(categories=['properties'])]
    assert traits == [base_common, base_a1, base_a2]
    traits = [trait for trait,cls in base.pyre_traits(mine=True, inherited=False)]
    assert traits == [base_common, base_a1, base_a2, base_do]
    traits = [trait for trait,cls in base.pyre_traits(mine=False, inherited=True)]
    assert traits == []
        
    # check a1
    # note that a1 is shadowed, so it needs special treatment
    traits = [trait for trait,cls in a1.pyre_traits()]
    assert traits == [a1_a1, a1_common, a1_a2, a1_do]
    traits = [trait for trait,cls in a1.pyre_traits(categories=['behaviors'])]
    assert traits == [a1_do]
    traits = [trait for trait,cls in a1.pyre_traits(categories=['properties'])]
    assert traits == [a1_a1, a1_common, a1_a2]
    traits = [trait for trait,cls in a1.pyre_traits(mine=True, inherited=False)]
    assert traits == [a1_a1]
    traits = [trait for trait,cls in a1.pyre_traits(mine=False, inherited=True)]
    assert traits == [a1_common, a1_a2, a1_do]

    # check a2
    # note that a2 is shadowed, so it needs special treatment
    traits = [trait for trait,cls in a2.pyre_traits()]
    assert traits == [a2_a2, a2_common, a2_a1, a2_do]
    traits = [trait for trait,cls in a2.pyre_traits(categories=['behaviors'])]
    assert traits == [a2_do]
    traits = [trait for trait,cls in a2.pyre_traits(categories=['properties'])]
    assert traits == [a2_a2, a2_common, a2_a1]
    traits = [trait for trait,cls in a2.pyre_traits(mine=True, inherited=False)]
    assert traits == [a2_a2]
    traits = [trait for trait,cls in a2.pyre_traits(mine=False, inherited=True)]
    assert traits == [a2_common, a2_a1, a2_do]

    # check derived: note extra traits and shadowing of the inherited ones
    traits = [trait for trait,cls in derived.pyre_traits()]
    assert traits == [derived_common, derived_extra, derived_do, derived_a1, derived_a2]
    traits = [trait for trait,cls in derived.pyre_traits(categories=['behaviors'])]
    assert traits == [derived_do]
    traits = [trait for trait,cls in derived.pyre_traits(categories=['properties'])]
    assert traits == [derived_common, derived_extra, derived_a1, derived_a2]
    traits = [trait for trait,cls in derived.pyre_traits(mine=True, inherited=False)]
    assert traits == [derived_common, derived_extra, derived_do]
    traits = [trait for trait,cls in derived.pyre_traits(mine=False, inherited=True)]
    assert traits == [a1_a1, a2_a2 ]
        
    return base, a1, a2, derived
     

# main
if __name__ == "__main__":
    test()


# end of file 
