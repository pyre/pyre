#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a protocol recognizes the components and component classes that come from classes
that declare they implement it, and nothing else
"""


# the driver
def test() -> None:
    """
    Ask a protocol about its implementers, the implementers of its relatives, and strangers
    """
    # support
    import pyre

    # a protocol
    class Base(pyre.protocol, family="implemented.bases"):
        """
        The base protocol
        """

        # a requirement
        common = pyre.properties.int()

    # one that refines it
    class Derived(Base, family="implemented.derived"):
        """
        A protocol that derives from the base
        """

    # an unrelated one
    class Other(pyre.protocol, family="implemented.others"):
        """
        A protocol of its own
        """

    # a component that implements the base
    class Plain(pyre.component, family="implemented.bases.plain", implements=Base):
        """
        An implementer of the base
        """

        # the requirement
        common = pyre.properties.int()

    # a subclass of it, which inherits the declaration
    class Heir(Plain, family="implemented.bases.heir"):
        """
        A subclass of an implementer
        """

    # a component that implements the refinement
    class Refined(pyre.component, family="implemented.derived.refined", implements=Derived):
        """
        An implementer of the derived protocol
        """

        # the requirement
        common = pyre.properties.int()

    # a component that implements two protocols
    class Both(pyre.component, family="implemented.both", implements=(Base, Other)):
        """
        An implementer of the base and of the other protocol
        """

        # the requirement
        common = pyre.properties.int()

    # a component that provides everything the base requires, but never says so
    class Lookalike(pyre.component, family="implemented.lookalike"):
        """
        A component that is compatible with the base but does not implement it
        """

        # the requirement
        common = pyre.properties.int()

    # implementers of the base are recognized, as classes and as instances
    for cls in (Plain, Heir, Refined, Both):
        # as a class
        assert Base.pyre_isImplementedBy(cls), cls
        # and as an instance
        assert Base.pyre_isImplementedBy(cls(name=f"implemented.{cls.__name__}")), cls
    # the derived protocol recognizes only the implementer of the derived protocol
    assert Derived.pyre_isImplementedBy(Refined)
    # and not the implementers of its ancestor, which are compatible with it for assignments
    assert not Derived.pyre_isImplementedBy(Plain)
    # including the one that implements both
    assert not Derived.pyre_isImplementedBy(Both)
    # the other protocol recognizes the component that implements both
    assert Other.pyre_isImplementedBy(Both)
    # and nothing else
    assert not Other.pyre_isImplementedBy(Plain)
    # a component that provides what the protocol requires
    assert Lookalike.pyre_isCompatible(Base)
    # but never declared it implements it is not recognized
    assert not Base.pyre_isImplementedBy(Lookalike)
    # and neither are its instances
    assert not Base.pyre_isImplementedBy(Lookalike(name="implemented.impostor"))
    # and neither is anything that is not a component
    for value in (None, 3, "implemented.bases.plain", Base, Derived):
        # check
        assert not Base.pyre_isImplementedBy(value), value

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
