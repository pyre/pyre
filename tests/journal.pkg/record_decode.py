#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Decoding refuses anything that is not a record, and says why
    """
    # access
    import journal

    # the exception decoding raises
    RecordError = journal.exceptions.RecordError
    # a well formed record to mutate
    good = {
        "journal": 1,
        "page": ["hello"],
        "notes": {"channel": "test", "severity": "info"},
    }

    # a helper that renders a variant and expects it to be refused
    def refuse(line):
        # attempt to
        try:
            # decode
            journal.record.decode(line)
        # if it was refused
        except RecordError as error:
            # the reason is part of the report
            assert error.reason
            # all good
            return
        # otherwise, it should not have been accepted
        assert False, f"accepted: {line!r}"

    # a helper that renders a variant of {good}
    def variant(**changes):
        # externals
        import json

        # a copy with the changes applied
        raw = {**good, **changes}
        # rendered
        return json.dumps(raw).encode("utf-8") + b"\n"

    # the baseline decodes
    assert journal.record.decode(variant()).page == ["hello"]

    # bytes that are not utf-8
    refuse(b"\xff\xfe\n")
    # text that is not json
    refuse(b"not json\n")
    # json that is not an object
    refuse(b"[1, 2, 3]\n")
    # a missing field
    refuse(b'{"journal": 1}\n')
    # the wrong version
    refuse(variant(journal=2))
    # a page that is not a list of strings
    refuse(variant(page="hello"))
    refuse(variant(page=[1, 2]))
    # notes that are not a map of strings
    refuse(variant(notes=["channel"]))
    refuse(variant(notes={"channel": 1}))

    # all done
    return


# main
if __name__ == "__main__":
    # tell journal to stay away from the bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
