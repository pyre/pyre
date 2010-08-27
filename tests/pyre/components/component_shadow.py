#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that property shadowing in derived components works as expected
"""


def test():
    import pyre

    # declare a couple of components
    class base(pyre.component):
        """the base component"""
        common = pyre.property()

    class derived(base):
        """the derived one"""
        common = pyre.property()
        
    # check the basics
    assert base.__name__ == "base"
    assert base.__bases__ == (pyre.component,)
    # check the layout
    assert base.pyre_name == "base"
    assert base.pyre_state == "registered"
    assert base.pyre_namemap == {'common': 'common'}
    assert base.pyre_pedigree == (base, pyre.component)
    # traits
    localNames = ['common']
    localTraits = tuple(map(base.pyre_getTraitDescriptor, localNames))
    assert base.pyre_traits == localTraits
    allNames = localNames + []
    allTraits = tuple(map(base.pyre_getTraitDescriptor, allNames))
    assert tuple(base.pyre_getTraitDescriptors()) == allTraits

    # check the basics
    assert derived.__name__ == "derived"
    assert derived.__bases__ == (base, )
    # check the layout
    assert derived.pyre_name == "derived"
    assert derived.pyre_state == "registered"
    assert derived.pyre_namemap == {'common': 'common'}
    assert derived.pyre_pedigree == (derived, base, pyre.component)
    # traits
    localNames = ['common']
    localTraits = tuple(map(derived.pyre_getTraitDescriptor, localNames))
    assert derived.pyre_traits == localTraits
    allNames = localNames + []
    allTraits = tuple(map(derived.pyre_getTraitDescriptor, allNames))
    assert tuple(derived.pyre_getTraitDescriptors()) == allTraits
    # make sure the two descriptors are not related
    assert base.pyre_getTraitDescriptor('common') is not derived.pyre_getTraitDescriptor('common')

    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
