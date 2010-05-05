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

    # collect the traits
    base_common = base.pyre_getTraitDescriptor("common")
    derived_common = derived.pyre_getTraitDescriptor("common")
    derived_extra = derived.pyre_getTraitDescriptor("extra")
    ok_common = ok.pyre_getTraitDescriptor("common")
    notok_what = notok.pyre_getTraitDescriptor("what")
    badtype_common = badtype.pyre_getTraitDescriptor("common")
    shadow_common = shadow.pyre_getTraitDescriptor("common")

    # compatibility checks
    # these ones should succeed
    assert derived.pyre_isCompatible(base)
    assert ok.pyre_isCompatible(base)
    assert derived.pyre_isCompatible(ok)

    # now the ones that should fail
    report = ok.pyre_isCompatible(derived, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[derived_extra][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = notok.pyre_isCompatible(base, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[base_common][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = notok.pyre_isCompatible(derived, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 2
    error = report.incompatibilities[derived_common][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)
    error = report.incompatibilities[derived_extra][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = notok.pyre_isCompatible(ok, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[ok_common][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = badtype.pyre_isCompatible(base, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[base_common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)

    report = badtype.pyre_isCompatible(derived, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 2
    error = report.incompatibilities[derived_common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)
    error = report.incompatibilities[derived_extra][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = badtype.pyre_isCompatible(ok, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[ok_common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)

    report = shadow.pyre_isCompatible(base, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[base_common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)

    report = shadow.pyre_isCompatible(derived, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 2
    error = report.incompatibilities[derived_common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)
    error = report.incompatibilities[derived_extra][0]
    assert isinstance(error, pyre.components.TraitNotFoundError)

    report = shadow.pyre_isCompatible(ok, createReport=True)
    assert not report
    assert len(report.incompatibilities) == 1
    error = report.incompatibilities[ok_common][0]
    assert isinstance(error, pyre.components.CategoryMismatchError)
        
    return base, derived, ok, notok, badtype, shadow


# main
if __name__ == "__main__":
    test()


# end of file 
