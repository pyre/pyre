#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A record survives the trip to its wire form and back, with every field intact
    """
    # access
    import journal

    # the parts of an entry
    page = ["first line", "  indented, with a\ttab", "and a non-ascii line: αβγ"]
    notes = {"channel": "test.record", "severity": "info", "application": "record_sanity"}
    # build a record by hand
    record = journal.record(page=page, notes=notes)
    # the identifying notes are reachable directly
    assert record.severity == "info"
    assert record.channel == "test.record"
    # and the sink follows from the severity
    assert record.sink == "alert"
    assert journal.record(page=[], notes={"severity": "debug"}).sink == "memo"
    assert journal.record(page=[], notes={"severity": "help"}).sink == "help"
    assert journal.record(page=[], notes={}).sink is None
    # unpacking yields the page and the notes
    assert tuple(record) == (page, notes)

    # its wire object has every field, in the declared order
    raw = record.raw()
    assert list(raw.keys()) == list(journal.record.fields)
    assert raw["journal"] == journal.record.version
    assert raw["page"] == page
    assert raw["notes"] == notes

    # its wire form is a single line
    line = record.encode()
    assert isinstance(line, bytes)
    assert line.endswith(b"\n")
    assert line.count(b"\n") == 1

    # the round trip
    clone = journal.record.decode(line)
    # preserves every field
    assert clone.page == page
    assert clone.notes == notes
    # and so does the round trip through text
    assert journal.record.decode(line.decode("utf-8")).page == page

    # a record stamped from a live entry carries the origin the caller supplies
    entry = journal.entry(notes=notes)
    # with some content
    entry.page.extend(page)
    # stamp it
    stamped = journal.record.stamp(entry=entry, pid=4242, seq=3, time=1.5, host="here")
    # check
    assert stamped.page == page
    # the notes are the entry's, plus the origin, as strings
    assert stamped.notes == {**notes, "pid": "4242", "seq": "3", "time": "1.5", "host": "here"}
    # the record holds copies, not the entry's containers
    assert stamped.page is not entry.page
    assert stamped.notes is not entry.notes
    # a note from the call site that uses an origin name is overwritten
    entry = journal.entry(notes={**notes, "time": "now"})
    assert journal.record.stamp(entry=entry, time=2.5).notes["time"] == "2.5"

    # all done
    return


# main
if __name__ == "__main__":
    # tell journal to stay away from the bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
