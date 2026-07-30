#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the requirement parser: category tags, flavor selectors, and version constraints
"""


def test():
    """
    Parse well formed requirements, evaluate their predicates, and check the error handling
    """
    # support
    import pyre.externals

    # get the requirement class and its syntax error
    requirement = pyre.externals.requirement
    syntaxError = requirement.RequirementSyntaxError

    # a bare category constrains nothing
    bare = requirement.parse("hdf5")
    # the category is harvested
    assert bare.category == "hdf5"
    # there are no selectors
    assert bare.selectors == () and bare.exclusions == ()
    # any flavor is admissible
    assert bare.admits(flavor="serial")
    # and any version is acceptable, even one we can't compare
    assert bare.accepts(version="1.8.0") and bare.accepts(version="unknown")

    # version clauses form a conjunction
    ranged = requirement.parse("hdf5>=1.12,<2")
    # the clauses are recorded in order
    assert ranged.clauses == ((">=", "1.12"), ("<", "2"))
    # versions inside the window pass
    assert ranged.accepts(version="1.12") and ranged.accepts(version="1.14.6")
    # versions outside the window fail
    assert not ranged.accepts(version="1.8.23") and not ranged.accepts(version="2.1.0")
    # comparisons are componentwise numeric, not lexicographic
    assert ranged.accepts(version="1.100")
    # a version we can't compare cannot be proven to satisfy the clauses
    assert not ranged.accepts(version="unknown") and not ranged.accepts(version="")

    # the remaining comparison operators
    assert requirement.parse("gsl==2.8").accepts(version="2.8")
    assert not requirement.parse("gsl==2.8").accepts(version="2.8.1")
    assert requirement.parse("gsl!=2.8").accepts(version="2.9")
    assert not requirement.parse("gsl!=2.8").accepts(version="2.8")
    assert requirement.parse("gsl<=2.8").accepts(version="2.8")
    assert requirement.parse("gsl>2.8").accepts(version="2.8.1")

    # alphabetic tails sort above their base component
    assert requirement.parse("gsl>1.14.6").accepts(version="1.14.6b")
    # purely alphabetic components sort below any numbered one
    assert not requirement.parse("gsl>=1.14.6").accepts(version="1.14.rc1")

    # flavor selectors must be answered by the flavor name or its class tags
    parallel = requirement.parse("hdf5[parallel]")
    # the selector is harvested
    assert parallel.selectors == ("parallel",)
    # the flavor name itself can answer
    assert parallel.admits(flavor="parallel")
    # or a class tag published by the recipe
    assert parallel.admits(flavor="openmpi", tags=("parallel",))
    # flavors with no matching name fail
    assert not parallel.admits(flavor="serial")

    # exclusions rule flavors out
    notSerial = requirement.parse("hdf5[!serial]")
    # the exclusion is harvested
    assert notSerial.exclusions == ("serial",)
    # excluded flavors are inadmissible
    assert not notSerial.admits(flavor="serial")
    # everything else passes
    assert notSerial.admits(flavor="openmpi", tags=("parallel",))

    # selectors and exclusions mix
    mixed = requirement.parse("hdf5[parallel, !mpich]")
    # an openmpi selection tagged parallel passes
    assert mixed.admits(flavor="openmpi", tags=("parallel",))
    # an mpich selection is ruled out even though it answers the selector
    assert not mixed.admits(flavor="mpich", tags=("parallel",))

    # the full grammar composes
    full = requirement.parse("hdf5[openmpi]>=1.14,<2")
    # all three sections are harvested
    assert full.category == "hdf5"
    assert full.selectors == ("openmpi",)
    assert full.clauses == ((">=", "1.14"), ("<", "2"))
    # and the normalized form reads back the same
    assert str(full) == "hdf5[openmpi]>=1.14,<2"

    # structured requirements pass through the parser untouched
    assert requirement.parse(full) is full

    # malformed specifications are rejected with the syntax error
    for bad in ("", "[openmpi]", "hdf5[]", "hdf5[!]", "hdf5[a,]", "hdf5=1.2", "hdf5>=", ">=1.2"):
        # attempt to
        try:
            # parse the broken spec
            requirement.parse(bad)
        # the parser must complain
        except syntaxError:
            # as expected
            pass
        # anything else is a failure
        else:
            # complain
            assert False, f"'{bad}' should not parse"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
