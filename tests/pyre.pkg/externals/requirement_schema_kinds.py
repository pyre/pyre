#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The requirement schema passes structured requirements through, parses text, and refuses every
other kind of value, and text it cannot parse with the parser's complaint
"""


def test() -> None:
    """
    Give the requirement schema a value of each kind, and check what becomes of it
    """
    # support
    import pyre
    from pyre.externals.Requirement import Requirement
    from pyre.externals.RequirementSchema import RequirementSchema

    # make a schema
    schema = RequirementSchema()

    # a structured requirement
    requirement = Requirement.parse(spec="mpi[openmpi]")
    # must pass through untouched
    assert schema.coerce(value=requirement) is requirement

    # text
    parsed = schema.coerce(value=" hdf5>=1.12 ")
    # must become a structured requirement
    assert isinstance(parsed, Requirement), repr(parsed)
    # with its sections harvested
    assert parsed.category == "hdf5" and parsed.clauses == ((">=", "1.12"),)

    # text the parser refuses
    for value in ["", "mpi[,]", "mpi[!]"]:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # with the parser's complaint
            assert isinstance(error.__cause__, Requirement.RequirementSyntaxError), value
            # as its own
            assert str(error) == str(error.__cause__), str(error)
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # kinds the schema does not support
    for value in [0, 5, 1.5, [], ["mpi"], {}, {"k": "v"}]:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # as a kind it does not support, so there is nothing behind the complaint
            assert error.__cause__ is None, f"{value!r}: {error.__cause__!r}"
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
