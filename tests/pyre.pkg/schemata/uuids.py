#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A universally unique identifier accepts identifiers and their text, and writes the canonical form
"""


def test() -> None:
    """
    Coerce an identifier and its text, and write it back
    """
    # support
    import uuid
    import pyre

    # make a schema
    schema = pyre.schemata.uuid()
    # an identifier
    identifier = uuid.UUID("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")

    # an identifier passes through
    assert schema.coerce(value=identifier) is identifier
    # its text, in any of the spellings python reads, is the same identifier
    assert schema.coerce(value="{A0EEBC99-9C0B-4EF8-BB6D-6BB9BD380A11}") == identifier
    # blank text is uninitialized
    assert schema.coerce(value="  ") is None
    # and the identifier writes its canonical form
    assert schema.string(identifier) == "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
