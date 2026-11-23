#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the conversions of the schema of json documents
"""


def test():
    """
    Convert text to documents and back, and refuse what is not one
    """
    # access the package
    import pyre

    # make a schema
    schema = pyre.schemata.json()
    # text is read as the json text of a document
    assert schema.coerce(value='{"a": [1, 2.5, null, true]}') == {"a": [1, 2.5, None, True]}
    # a document is taken as it is
    assert schema.coerce(value={"b": "it's"}) == {"b": "it's"}
    # and rendered as its json text
    assert schema.string(value={"a": [1, None]}) == '{"a": [1, null]}'
    # text that is not json
    try:
        # cannot be read
        schema.coerce(value="{not json")
    # so it is refused
    except schema.CastingError:
        # as expected
        pass
    # if it isn't
    else:
        # complain
        assert False, "text that is not json was read as a document"
    # and so is a value json cannot write
    try:
        # such as a set
        schema.coerce(value={1, 2})
    # which is refused
    except schema.CastingError:
        # as expected
        pass
    # if it isn't
    else:
        # complain
        assert False, "a set was taken as a json document"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
