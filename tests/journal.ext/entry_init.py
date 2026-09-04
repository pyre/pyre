#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    An entry can be built with a given page and notes, from native or bound containers
    """
    # access
    from journal import libjournal

    # the content
    page = ["first", "  second", "third: αβγ"]
    notes = {"channel": "test.entry", "severity": "info", "application": "entry_init"}

    # build an entry from native containers
    entry = libjournal.Entry(page=page, notes=notes)
    # the page is what was supplied
    assert list(entry.page) == page
    # and so are the notes, with nothing else mixed in
    assert dict(entry.notes) == notes

    # build another from the bound containers of the first
    clone = libjournal.Entry(page=entry.page, notes=entry.notes)
    # check
    assert list(clone.page) == page
    assert dict(clone.notes) == notes

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
