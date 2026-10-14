#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sequences render as the text they read, and leave out the items they can't convert,
with a warning
"""


def test() -> None:
    """
    Render sequences as text, read them back, and coerce text with bad items
    """
    # support
    import journal
    import pyre.schemata

    # a list of strings
    strings = pyre.schemata.list(schema=pyre.schemata.str())
    # and a tuple of integers
    integers = pyre.schemata.tuple(schema=pyre.schemata.int())

    # sequences render as text
    assert strings.string(["a", "b"]) == "a, b"
    assert integers.string((1, 2)) == "1, 2"
    # which reads back as the same sequence
    assert strings.coerce(strings.string(["a", "b"])) == ["a", "b"]
    assert integers.coerce(integers.string((1, 2))) == (1, 2)
    # and {None} is left alone
    assert strings.string(None) is None

    # items that can't be converted are left out, with a warning; send the warnings to a file
    journal.warning("pyre.config.containers").device = journal.file(path="lists_text.log")
    # so text with a bad item
    assert integers.coerce("1, x, 3") == (1, 3)
    # loses it
    with open("lists_text.log") as log:
        # and the report
        report = log.read()
    # names it
    assert "skipping 'x'" in report, report

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
