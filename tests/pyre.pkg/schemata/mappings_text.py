#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that mappings read their text form, "key:value, key:value", and write it back
"""


def test() -> None:
    """
    Coerce text into mappings, render mappings as text, and leave out what can't be used
    """
    # support
    import journal
    import pyre.schemata

    # a mapping of strings
    strings = pyre.schemata.mapping(schema=pyre.schemata.str())
    # and one of integers
    integers = pyre.schemata.mapping(schema=pyre.schemata.int())

    # text is split into entries at the commas, and each entry at its first colon
    assert strings.coerce("band:L, frequency:A") == {"band": "L", "frequency": "A"}
    # so values may hold colons of their own
    assert strings.coerce("uri:s3://bucket/key") == {"uri": "s3://bucket/key"}
    # the space around keys and values is not part of them, and blank entries are skipped
    assert strings.coerce(" band : L ,, frequency:A, ") == {"band": "L", "frequency": "A"}
    # empty text is an empty mapping
    assert strings.coerce("") == {}
    # and the values are converted by the schema of the entries
    assert integers.coerce("one:1, two:2") == {"one": 1, "two": 2}

    # the text form names the type of the entries
    assert strings.type == "mapping[str]"
    # mappings render as their text form
    assert strings.string({"band": "L", "frequency": "A"}) == "band:L, frequency:A"
    # which reads back as the same mapping
    assert strings.coerce(strings.string({"band": "L", "frequency": "A"})) == {
        "band": "L",
        "frequency": "A",
    }
    # their values are rendered by the schema of the entries
    assert integers.json({"one": 1}) == {"one": 1}
    # and {None} is left alone
    assert strings.string(None) is None

    # keys are strings, as they are in configuration files
    assert strings.coerce({1: "one"}) == {"1": "one"}

    # entries that can't be used are left out, with a warning; send the warnings to a file
    journal.warning("pyre.config.containers").device = journal.file(path="mappings_text.log")
    # an entry without a key
    assert strings.coerce("band, frequency:A, :B") == {"frequency": "A"}
    # anything in an iterable that isn't a pair, such as a string, which would unpack as one
    assert strings.coerce(["ab", ("band", "L")]) == {"band": "L"}
    # and a value that can't be converted
    assert integers.coerce("one:1, two:x") == {"one": 1}
    # each of them was reported
    with open("mappings_text.log") as log:
        # so read the report
        report = log.read()
    # and look for each one
    for entry in ("'band'", "':B'", "'ab'", "'two:x'"):
        # by name
        assert f"skipping {entry}" in report, report

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
