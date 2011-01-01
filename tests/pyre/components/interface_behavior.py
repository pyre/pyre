#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Check that interfaces with behaviors have the expected layout
"""


def test():
    import pyre

    class interface(pyre.interface):
        """a trivial interface"""
        @pyre.provides
        def do(self):
            """trivial behavior"""

    # checks
    # check the basics
    assert interface.__name__ == "interface"
    assert interface.__bases__ == (pyre.interface,)
    # check the layout
    assert interface.pyre_name == "interface"
    assert interface.pyre_pedigree == [interface, pyre.interface]
    # traits
    localNames = ['do']
    localTraits = list(map(interface.pyre_getTraitDescriptor, localNames))
    assert interface.pyre_localTraits == localTraits
    assert interface.pyre_inheritedTraits == []
    allNames = localNames + []
    allTraits = list(map(interface.pyre_getTraitDescriptor, allNames))
    assert list(interface.pyre_getTraitDescriptors()) == allTraits
    

    return interface


# main
if __name__ == "__main__":
    test()


# end of file 
