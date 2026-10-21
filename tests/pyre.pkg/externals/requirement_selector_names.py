#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Selectors and exclusions must be flavor names: a letter followed by letters, digits, and any of
{_}, {-} and {.}; anything else raises the syntax error, with the name in the complaint
"""


def test() -> None:
    """
    Feed the parser selectors with good names and bad ones
    """
    # support
    import pyre.externals

    # get the requirement class and its syntax error
    requirement = pyre.externals.requirement
    syntaxError = requirement.RequirementSyntaxError

    # specifications with good names, and the selectors and exclusions they must yield
    good = [
        ("mpi[openmpi]", ("openmpi",), ()),
        ("hdf5[hdf5-openmpi]", ("hdf5-openmpi",), ()),
        ("python[python3]", ("python3",), ()),
        ("gcc[gcc12.2, a_b]", ("gcc12.2", "a_b"), ()),
        ("hdf5[parallel, !mpich]", ("parallel",), ("mpich",)),
        ("hdf5[! serial]", (), ("serial",)),
    ]
    # go through them
    for spec, selectors, exclusions in good:
        # parse each one
        parsed = requirement.parse(spec)
        # it must yield the expected selectors
        assert parsed.selectors == selectors, f"{spec}: {parsed.selectors}"
        # and exclusions
        assert parsed.exclusions == exclusions, f"{spec}: {parsed.exclusions}"

    # specifications with bad names, and the name each complaint must mention
    bad = [
        ("mpi[}]", "}"),
        ("mpi[!}]", "}"),
        ("mpi[{x}]", "{x}"),
        ("mpi[open mpi]", "open mpi"),
        ("mpi[3mpi]", "3mpi"),
        ("mpi[parallel, $]", "$"),
        ("mpi[!-x]", "-x"),
    ]
    # go through them
    for spec, name in bad:
        # attempt to
        try:
            # parse each one
            requirement.parse(spec)
        # the parser must complain
        except syntaxError as error:
            # about the name
            assert f"'{name}'" in str(error), f"{spec}: {error}"
        # anything else is a failure
        else:
            # complain
            assert False, f"'{spec}' should not parse"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
