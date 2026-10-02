#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the debug channels named in {JOURNAL_DEBUG} start out active
    """
    # access
    import journal

    # the channels named in the environment are active
    assert journal.debug("tests.journal.env.one").active
    assert journal.debug("tests.journal.env.two").active
    # and the others are not
    assert not journal.debug("tests.journal.env.three").active

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
