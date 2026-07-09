#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check whether file iterators are synchronized with independent accesses to the file object
"""


def test():
    # one line at a time
    single = 0
    with open("files.py") as f:
        for line in f:
            single += 1

    # two lines at a time
    double = 0
    with open("files.py") as f:
        for line in f:
            double += 1
            # the extra read that shouldn't de-sync the iterator
            extra = f.readline()
            double += 1

    # check
    assert single == double

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
