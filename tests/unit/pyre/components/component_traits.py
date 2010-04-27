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

        @pyre.components.export
        def do(self):
            """behave"""

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

        @pyre.components.export
        def do(self):
            """behave"""


    # check base
    traits = [trait for trait,cls in base.pyre_traits()]
    assert traits == [base.common, base.a1, base.a2, base.do]
    traits = [trait for trait,cls in base.pyre_traits(categories=['behaviors'])]
    assert traits == [base.do]
    traits = [trait for trait,cls in base.pyre_traits(categories=['properties'])]
    assert traits == [base.common, base.a1, base.a2]
    traits = [trait for trait,cls in base.pyre_traits(mine=True, inherited=False)]
    assert traits == [base.common, base.a1, base.a2, base.do]
    traits = [trait for trait,cls in base.pyre_traits(mine=False, inherited=True)]
    assert traits == []
        
    # check a1
    # note that a1 is shadowed, so it needs special treatment
    traits = [trait for trait,cls in a1.pyre_traits()]
    assert traits == [a1.a1, a1.common, a1.a2, a1.do]
    traits = [trait for trait,cls in a1.pyre_traits(categories=['behaviors'])]
    assert traits == [a1.do]
    traits = [trait for trait,cls in a1.pyre_traits(categories=['properties'])]
    assert traits == [a1.a1, a1.common, a1.a2]
    traits = [trait for trait,cls in a1.pyre_traits(mine=True, inherited=False)]
    assert traits == [a1.a1]
    traits = [trait for trait,cls in a1.pyre_traits(mine=False, inherited=True)]
    assert traits == [a1.common, a1.a2, a1.do]

    # check a2
    # note that a2 is shadowed, so it needs special treatment
    traits = [trait for trait,cls in a2.pyre_traits()]
    assert traits == [a2.a2, a2.common, a2.a1, a2.do]
    traits = [trait for trait,cls in a2.pyre_traits(categories=['behaviors'])]
    assert traits == [a2.do]
    traits = [trait for trait,cls in a2.pyre_traits(categories=['properties'])]
    assert traits == [a2.a2, a2.common, a2.a1]
    traits = [trait for trait,cls in a2.pyre_traits(mine=True, inherited=False)]
    assert traits == [a2.a2]
    traits = [trait for trait,cls in a2.pyre_traits(mine=False, inherited=True)]
    assert traits == [a2.common, a2.a1, a2.do]

    # check derived: note extra traits and shadowing of the inherited ones
    traits = [trait for trait,cls in derived.pyre_traits()]
    assert traits == [derived.common, derived.extra, derived.do, derived.a1, derived.a2]
    traits = [trait for trait,cls in derived.pyre_traits(categories=['behaviors'])]
    assert traits == [derived.do]
    traits = [trait for trait,cls in derived.pyre_traits(categories=['properties'])]
    assert traits == [derived.common, derived.extra, derived.a1, derived.a2]
    traits = [trait for trait,cls in derived.pyre_traits(mine=True, inherited=False)]
    assert traits == [derived.common, derived.extra, derived.do]
    traits = [trait for trait,cls in derived.pyre_traits(mine=False, inherited=True)]
    assert traits == [a1.a1, a2.a2]
        
    return base, a1, a2, derived
     

# main
if __name__ == "__main__":
    test()


# end of file 
