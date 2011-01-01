#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the inheritnace invariants are respected
"""


def test():
    import pyre

    # declare a couple of interfaces
    class base(pyre.interface):
        """the base interface"""
        common = pyre.property()

    class derived(base):
        """the derived one"""
        extra = pyre.property()
        
    # check the basics
    assert base.__name__ == "base"
    assert base.__bases__ == (pyre.interface,)
    # check the layout
    assert base.pyre_name == "base"
    assert base.pyre_namemap == {'common': 'common'}
    assert base.pyre_pedigree == [base, pyre.interface]
    # traits
    localNames = ['common']
    localTraits = list(map(base.pyre_getTraitDescriptor, localNames))
    assert base.pyre_localTraits == localTraits
    assert base.pyre_inheritedTraits == []
    allNames = localNames + []
    allTraits = list(map(base.pyre_getTraitDescriptor, allNames))
    assert list(base.pyre_getTraitDescriptors()) == allTraits

    # check the basics
    assert derived.__name__ == "derived"
    assert derived.__bases__ == (base, )
    # check the layout
    assert derived.pyre_name == "derived"
    assert derived.pyre_namemap == {
        'common': 'common', 'extra': 'extra'
        }
    assert derived.pyre_pedigree == [derived, base, pyre.interface]
    # traits
    localNames = ['extra']
    localTraits = list(map(derived.pyre_getTraitDescriptor, localNames))
    assert derived.pyre_localTraits == localTraits
    inheritedNames = ['common']
    inheritedTraits = list(map(derived.pyre_getTraitDescriptor, inheritedNames))
    assert derived.pyre_inheritedTraits == inheritedTraits
    allNames = localNames + ['common']
    allTraits = list(map(derived.pyre_getTraitDescriptor, allNames))
    assert list(derived.pyre_getTraitDescriptors()) == allTraits

    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
