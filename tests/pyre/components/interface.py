#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Check that declarations of trivial interfaces produce the expected layout
"""


def test():
    import pyre

    # declare
    class interface(pyre.interface):
        """a trivial interface"""

    # check the basics
    assert interface.__name__ == "interface"
    assert interface.__bases__ == (pyre.interface,)

    # check the layout
    assert interface.pyre_name == "interface"
    assert interface.pyre_family == []
    assert interface.pyre_namemap == {}
    assert interface.pyre_localTraits == []
    assert interface.pyre_inheritedTraits == []
    assert interface.pyre_pedigree == [interface, pyre.interface]

    # exercise the configurable interface
    assert tuple(interface.pyre_getTraitDescriptors()) == ()
    assert interface.pyre_isCompatible(interface)

    return interface


# main
if __name__ == "__main__":
    test()


# end of file 
