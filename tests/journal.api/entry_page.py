#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test() -> None:
    """
    Verify that an entry built with a page keeps a copy of it
    """
    # access
    import journal

    # a page
    page = ["hello", "world"]
    # build an entry with it
    entry = journal.entry(notes={}, page=page)
    # change the original
    page.append("again")
    # the entry kept the page as it was
    assert list(entry.page) == ["hello", "world"]

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
