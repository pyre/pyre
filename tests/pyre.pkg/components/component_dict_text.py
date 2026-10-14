#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dict trait accepts its text form, "key:value, key:value", converts each value with
the schema of its entries, and runs its validators
"""


def test() -> None:
    """
    Assign text, dicts, and the representations of {None} to dict traits
    """
    # support
    import journal
    import pyre

    # the maps the validator was shown
    shown = []

    # a validator that records what it is shown
    def record(value, **kwds):
        """
        Record {value} and let it through
        """
        # make a copy
        shown.append(dict(value))
        # and let it through
        return value

    # a component with dicts of strings and of integers
    class Reader(pyre.component, family="pyre.tests.dict.text.reader"):
        """
        A component with dict traits
        """

        # a map of strings, with a validator
        selection = pyre.properties.kv()
        selection.validators = record
        # and a map of integers
        counts = pyre.properties.dict(schema=pyre.properties.int())

    # a dict is a mapping, and says what its values are
    assert Reader.pyre_trait("selection").type == "dict[str]"
    # including when they are not strings
    assert Reader.pyre_trait("counts").type == "dict[int]"

    # make a reader
    reader = Reader(name="reader")

    # assign text
    reader.selection = "band:L, frequency:A, uri:s3://bucket/key"
    # which is split into entries, each at its first colon
    assert dict(reader.selection) == {"band": "L", "frequency": "A", "uri": "s3://bucket/key"}
    # and the validator was shown the map
    assert shown[-1] == {"band": "L", "frequency": "A", "uri": "s3://bucket/key"}
    # and it renders back as text
    assert Reader.pyre_trait("selection").string(reader.selection) == (
        "band:L, frequency:A, uri:s3://bucket/key"
    )

    # text can be checked without storing it anywhere, the way it is for any other property
    checked = Reader.pyre_trait("counts").coerce(value="one:1, two:2")
    # which makes a plain dictionary, with its values converted
    assert type(checked) is dict and checked == {"one": 1, "two": 2}

    # the values of the entries are converted by their schema, here as expressions
    reader.counts = "one:1, two:1+1"
    # so they are integers
    assert dict(reader.counts) == {"one": 1, "two": 2}

    # assigning a dict replaces the map
    reader.selection = {"polarization": "HH"}
    # so the entries that are not in it are gone
    assert dict(reader.selection) == {"polarization": "HH"}

    # empty text
    reader.selection = ""
    # is an empty map
    assert dict(reader.selection) == {}
    # while the text form of {None}
    reader.selection = "none"
    # is {None}
    assert reader.selection is None

    # entries that can't be used are left out, with a warning; send the warnings to a file
    journal.warning("pyre.config.containers").device = journal.file(path="component_dict_text.log")
    # an entry without a key, and one whose key holds the separator of the store
    reader.selection = "band, frequency:A, a.b:c"
    # are left out
    assert dict(reader.selection) == {"frequency": "A"}
    # and reported
    with open("component_dict_text.log") as log:
        # so read the report
        report = log.read()
    # and look for each one
    for entry in ("'band'", "'a.b'"):
        # by name
        assert f"skipping {entry}" in report, report

    # a value that is not a map at all
    reader.selection = 5
    # is accepted, since values are converted when they are read
    try:
        # so reading it
        reader.selection
        # must fail
        assert False, "5 was accepted as a map"
    # with a casting error
    except Reader.pyre_trait("selection").CastingError:
        # as expected
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
