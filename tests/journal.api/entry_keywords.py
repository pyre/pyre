#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test() -> None:
    """
    Verify that the parts of an entry are passed by keyword only, so that no implementation can
    read them in the wrong order
    """
    # access
    import journal

    # building an entry from positional arguments
    try:
        # should fail
        journal.entry({}, [])
    # with a type error
    except TypeError:
        # as it should
        pass
    # if it doesn't
    else:
        # the parts can be confused
        assert False, "an entry accepted its parts by position"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
