#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Malformed requirement specifications raise the syntax error
"""


def test():
    """
    Feed the parser broken specifications and verify each is rejected
    """
    # support
    import pyre.externals

    # get the requirement class and its syntax error
    requirement = pyre.externals.requirement
    syntaxError = requirement.RequirementSyntaxError

    # the pile of malformed specifications
    broken = (
        # nothing at all
        "",
        # no category ahead of the selectors
        "[openmpi]",
        # empty selector section
        "hdf5[]",
        # empty exclusion
        "hdf5[!]",
        # trailing empty selector
        "hdf5[a,]",
        # a single {=} is not a comparison
        "hdf5=1.2",
        # an operator with no version
        "hdf5>=",
        # no category ahead of the version clauses
        ">=1.2",
    )
    # go through them
    for bad in broken:
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
