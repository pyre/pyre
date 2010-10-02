#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
    assert base.pyre_state == "registered"
    assert base.pyre_namemap == {'common': 'common'}
    assert base.pyre_pedigree == (base, pyre.interface)
    # traits
    localNames = ['common']
    localTraits = tuple(map(base.pyre_getTraitDescriptor, localNames))
    assert base.pyre_localTraits == localTraits
    assert base.pyre_inheritedTraits == ()
    allNames = localNames + []
    allTraits = tuple(map(base.pyre_getTraitDescriptor, allNames))
    assert tuple(base.pyre_getTraitDescriptors()) == allTraits

    # check the basics
    assert derived.__name__ == "derived"
    assert derived.__bases__ == (base, )
    # check the layout
    assert derived.pyre_name == "derived"
    assert derived.pyre_state == "registered"
    assert derived.pyre_namemap == {'extra': 'extra'}
    assert derived.pyre_pedigree == (derived, base, pyre.interface)
    # traits
    localNames = ['extra']
    localTraits = tuple(map(derived.pyre_getTraitDescriptor, localNames))
    assert derived.pyre_localTraits == localTraits
    inheritedNames = ['common']
    inheritedTraits = tuple(map(derived.pyre_getTraitDescriptor, inheritedNames))
    assert derived.pyre_inheritedTraits == inheritedTraits
    allNames = localNames + ['common']
    allTraits = tuple(map(derived.pyre_getTraitDescriptor, allNames))
    assert tuple(derived.pyre_getTraitDescriptors()) == allTraits

    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
