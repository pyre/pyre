#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an instance reads a trait it inherits through a mixin without a family that
precedes the ancestor that declares it
"""


def test() -> None:
    """
    Read a trait declared on an ancestor that a family-less mixin precedes in the pedigree
    """
    # support
    import pyre

    # a base component with a family
    class base(pyre.component, family="pyre.tests.mixin.base"):
        """the base component"""

        # that declares a trait of its own
        common = pyre.properties.str()
        common.default = "common"

    # a mixin without a family, so it has a private inventory
    class single(base):
        """a mixin that declares nothing"""

    # a mixin with a family that declares the trait of interest
    class archival(base, family="pyre.tests.mixin.archival"):
        """the ancestor that declares {archive}"""

        # the trait of interest
        archive = pyre.properties.str()
        archive.default = "ops"

    # a component that puts the family-less mixin ahead of the declaring one
    class derived(single, archival, family="pyre.tests.mixin.derived"):
        """the derived component"""

    # get the trait of interest
    archive = derived.pyre_trait(alias="archive")
    # verify the pedigree puts the family-less mixin ahead of the declaring ancestor
    assert derived.pyre_pedigree == (derived, single, archival, base, pyre.component)
    # verify that {derived} finds the slot of {archive} in the ancestor that declares it
    assert derived.pyre_inventory.inheritedFrom(component=derived, trait=archive) is archival
    # verify that the declaring ancestor owns it
    assert archival.pyre_inventory.inheritedFrom(component=archival, trait=archive) is None

    # make an instance
    instance = derived(name="instance")
    # verify that it reads the default of the declaring ancestor
    assert instance.archive == "ops"
    # and that it reads the trait of the base through the mixin as well
    assert instance.common == "common"
    # verify that the value it kept carries the provenance of the declaring ancestor
    assert instance.pyre_traitSource(trait=archive) == archival.pyre_classTraitSource(trait=archive)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
