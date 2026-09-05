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
    record = journal.record(sink="alert", page=page, notes=notes, seq=7, pid=4242, time=1.5)
    # the identifying notes are reachable directly
    assert record.severity == "info"
    assert record.channel == "test.record"
    # unpacking yields the page and the notes
    assert tuple(record) == (page, notes)

    # its wire object has every field, in the declared order
    raw = record.raw()
    assert list(raw.keys()) == list(journal.record.fields)
    assert raw["journal"] == journal.record.version
    assert raw["sink"] == "alert"
    assert raw["page"] == page
    assert raw["notes"] == notes
    assert (raw["seq"], raw["pid"], raw["time"]) == (7, 4242, 1.5)

    # its wire form is a single line
    line = record.encode()
    assert isinstance(line, bytes)
    assert line.endswith(b"\n")
    assert line.count(b"\n") == 1

    # the round trip
    clone = journal.record.decode(line)
    # preserves every field
    assert clone.sink == "alert"
    assert clone.page == page
    assert clone.notes == notes
    assert clone.seq == 7
    assert clone.pid == 4242
    assert clone.time == 1.5
    # and so does the round trip through text
    assert journal.record.decode(line.decode("utf-8")).page == page

    # a record stamped from a live entry carries the current process and time
    import os
    import time

    # make an entry
    entry = journal.entry(notes=notes)
    # with some content
    entry.page.extend(page)
    # stamp it
    before = time.time()
    stamped = journal.record.stamp(entry=entry, sink="memo", seq=3)
    after = time.time()
    # check
    assert stamped.sink == "memo"
    assert stamped.page == page
    assert stamped.notes == notes
    assert stamped.seq == 3
    assert stamped.pid == os.getpid()
    assert before <= stamped.time <= after
    # the record holds copies, not the entry's containers
    assert stamped.page is not entry.page
    assert stamped.notes is not entry.notes

    # all done
    return


# main
if __name__ == "__main__":
    # tell journal to stay away from the bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
