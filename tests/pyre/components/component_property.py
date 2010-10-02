#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    import pyre

    class component(pyre.component):
        """a trivial component"""
        p = pyre.property()

    # check the basics
    assert component.__name__ == "component"
    assert component.__bases__ == (pyre.component,)
    # check the layout
    assert component.pyre_name == "component"
    assert component.pyre_state == "registered"
    assert component.pyre_namemap == {'p': 'p'}
    assert component.pyre_pedigree == (component, pyre.component)
    assert component.pyre_family == []
    assert component.pyre_implements == None
    # traits
    localNames = ['p']
    localTraits = tuple(map(component.pyre_getTraitDescriptor, localNames))
    assert component.pyre_localTraits == localTraits
    assert component.pyre_inheritedTraits == ()
    allNames = localNames + []
    allTraits = tuple(map(component.pyre_getTraitDescriptor, allNames))
    assert tuple(component.pyre_getTraitDescriptors()) == allTraits

    return component


# main
if __name__ == "__main__":
    test()


# end of file 
