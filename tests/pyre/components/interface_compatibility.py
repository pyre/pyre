#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the interface compatibility checks are implemented correctly
"""


def test():
    # access
    import pyre.components
    from pyre.components.Property import Property
    from pyre.components.Interface import Interface

    # declare some interfaces
    class base(Interface):
        """a base interface"""
        common = Property()

    class derived(base):
        """a derived interface, so automatically compatible"""
        extra = Property()

    class ok(Interface):
        """one that doesn't, but provides the correct public interface"""
        common = Property()
        
    class notok(Interface):
        """one that doesn't provide the correct public interface"""
        what = Property()

    class badtype(Interface):
        """one that has the right trait, but of the wrong category"""
        @pyre.components.provides
        def common(self):
            """method, not property"""
        
    class shadow(base):
        """one that has derives, but shadows the trait in an incompatible way"""
        @pyre.components.provides
        def common(self):
            """method, not property"""

    # compatibility checks
    # the ones that should succeed
    assert derived.pyre_isCompatible(base)
    assert ok.pyre_isCompatible(base)
    assert derived.pyre_isCompatible(ok)
    # and the ones that should fail
    assert not ok.pyre_isCompatible(derived)
    assert not notok.pyre_isCompatible(base)
    assert not notok.pyre_isCompatible(derived)
    assert not notok.pyre_isCompatible(ok)
    assert not badtype.pyre_isCompatible(base)
    assert not badtype.pyre_isCompatible(derived)
    assert not badtype.pyre_isCompatible(ok)
    assert not shadow.pyre_isCompatible(base)
    assert not shadow.pyre_isCompatible(derived)
    assert not shadow.pyre_isCompatible(ok)
        
    return base, derived, ok, notok, badtype, shadow


# main
if __name__ == "__main__":
    test()


# end of file 
