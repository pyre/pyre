#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Verify that compatibility among protocols is detected correctly
"""


def test():
    import pyre

    # declare a couple of protocols
    class base(pyre.protocol):
        """the base protocol"""
        common = pyre.properties.int()

    class derived(base):
        """a derived one, so automatically compatible"""
        extra = pyre.properties.int()

    class ok(pyre.protocol):
        """one that doesn't derive but has the right public protocol"""
        common = pyre.properties.int()

    class notok(pyre.protocol):
        """one that doesn't provide the right public protocol"""
        what = pyre.properties.int()

    class badtype(pyre.protocol):
        """one that has the right trait but of the wrong type"""
        @pyre.provides
        def common(self):
            """method, not property"""

    class shadow(base):
        """one that derives but shadows the trait in an incompatible way"""
        @pyre.provides
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
