#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the component compatibility checks are implemented correctly
"""


def test():
    # access
    import pyre.components
    from pyre.components.Property import Property
    from pyre.components.Component import Component

    # declare some components
    class base(Component):
        """a base component"""
        common = Property()
        common.default = "base"

    class derived(base):
        """a derived component, so automatically compatible"""
        extra = Property()
        extra.default = "derived"

    class ok(Component):
        """one that doesn't, but provides the correct public component"""
        common = Property()
        common.default = "ok"
        
    class notok(Component):
        """one that doesn't provide the correct public component"""
        what = Property()
        what.default = "notok"

    class badtype(Component):
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
    # these ones should succeed
    assert derived.pyre_isCompatible(base)
    assert ok.pyre_isCompatible(base)
    assert derived.pyre_isCompatible(ok)

    # now the ones that should fail
    report = ok.pyre_isCompatible(derived, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[derived.extra][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = notok.pyre_isCompatible(base, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[base.common][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = notok.pyre_isCompatible(derived, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 2
    error = report.incompatibilities[derived.common][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)
    error = report.incompatibilities[derived.extra][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = notok.pyre_isCompatible(ok, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[ok.common][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = badtype.pyre_isCompatible(base, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[base.common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)

    report = badtype.pyre_isCompatible(derived, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 2
    error = report.incompatibilities[derived.common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)
    error = report.incompatibilities[derived.extra][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = badtype.pyre_isCompatible(ok, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[ok.common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)

    report = shadow.pyre_isCompatible(base, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[base.common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)

    report = shadow.pyre_isCompatible(derived, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 2
    error = report.incompatibilities[derived.common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)
    error = report.incompatibilities[derived.extra][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = shadow.pyre_isCompatible(ok, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[ok.common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)
        
    return base, derived, ok, notok, badtype, shadow


# main
if __name__ == "__main__":
    test()


# end of file 
