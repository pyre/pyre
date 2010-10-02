#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that multiple inheritance is treated properly
"""


def test():
    import pyre

    # declare a couple of components
    class base(pyre.component):
        """the base component"""
        common = pyre.property()
        a1 = pyre.property()
        a2 = pyre.property()

    class a1(base):
        a1 = pyre.property()

    class a2(base):
        a2 = pyre.property()

    class derived(a1, a2):
        """the derived one"""
        common = pyre.property()
        extra = pyre.property()
        
    # check the basics
    assert base.__name__ == "base"
    assert base.__bases__ == (pyre.component,)
    # check the layout
    assert base.pyre_name == "base"
    assert base.pyre_state == "registered"
    assert base.pyre_namemap == {'common':'common', 'a1':'a1', 'a2':'a2'}
    assert base.pyre_pedigree == (base, pyre.component)
    # traits
    localNames = ['common', 'a1', 'a2']
    localTraits = tuple(map(base.pyre_getTraitDescriptor, localNames))
    assert base.pyre_localTraits == localTraits
    assert base.pyre_inheritedTraits == ()
    allNames = localNames + []
    allTraits = tuple(map(base.pyre_getTraitDescriptor, allNames))
    assert tuple(base.pyre_getTraitDescriptors()) == allTraits

    # check the basics
    assert a1.__name__ == "a1"
    assert a1.__bases__ == (base,)
    # check the layout
    assert a1.pyre_name == "a1"
    assert a1.pyre_state == "registered"
    assert a1.pyre_namemap == {'a1':'a1'}
    assert a1.pyre_pedigree == (a1, base, pyre.component)
    # traits
    localNames = ['a1']
    localTraits = tuple(map(a1.pyre_getTraitDescriptor, localNames))
    assert a1.pyre_localTraits == localTraits
    inheritedNames = ['common', 'a2']
    inheritedTraits = tuple(map(a1.pyre_getTraitDescriptor, inheritedNames))
    assert a1.pyre_inheritedTraits == inheritedTraits
    allNames = localNames + ['common', 'a2']
    allTraits = tuple(map(a1.pyre_getTraitDescriptor, allNames))
    assert tuple(a1.pyre_getTraitDescriptors()) == allTraits

    # check the basics
    assert a2.__name__ == "a2"
    assert a2.__bases__ == (base,)
    # check the layout
    assert a2.pyre_name == "a2"
    assert a2.pyre_state == "registered"
    assert a2.pyre_namemap == {'a2':'a2'}
    assert a2.pyre_pedigree == (a2, base, pyre.component)
    # traits
    localNames = ['a2']
    localTraits = tuple(map(a2.pyre_getTraitDescriptor, localNames))
    assert a2.pyre_localTraits == localTraits
    inheritedNames = ['common', 'a1']
    inheritedTraits = tuple(map(a2.pyre_getTraitDescriptor, inheritedNames))
    assert a2.pyre_inheritedTraits == inheritedTraits
    allNames = localNames + ['common', 'a1']
    allTraits = tuple(map(a2.pyre_getTraitDescriptor, allNames))
    assert tuple(a2.pyre_getTraitDescriptors()) == allTraits

    # check the basics
    assert derived.__name__ == "derived"
    assert derived.__bases__ == (a1, a2)
    # check the layout
    assert derived.pyre_name == "derived"
    assert derived.pyre_state == "registered"
    assert derived.pyre_namemap == {'common':'common', 'extra':'extra'}
    assert derived.pyre_pedigree == (derived, a1, a2, base, pyre.component)
    # traits
    localNames = ['common', 'extra']
    localTraits = tuple(map(derived.pyre_getTraitDescriptor, localNames))
    assert derived.pyre_localTraits == localTraits
    inheritedNames = ['a1', 'a2']
    inheritedTraits = tuple(map(derived.pyre_getTraitDescriptor, inheritedNames))
    assert derived.pyre_inheritedTraits == inheritedTraits
    allNames = localNames + ['a1', 'a2']
    allTraits = tuple(map(derived.pyre_getTraitDescriptor, allNames))
    assert tuple(derived.pyre_getTraitDescriptors()) == allTraits

    return base, a1, a2, derived


# main
if __name__ == "__main__":
    test()


# end of file 
