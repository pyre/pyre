#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Check that a file the library would not open answers every question with nothing: no
    member at any path, no members at all. The answers come from the library's refusal, never
    from metadata it never wrote, so they hold whatever the stack happens to contain
    """
    # get the bindings
    from pyre.extensions import libh5

    # for the scratch file
    import os

    # a file that is not h5 at all
    uri = "h5_ext_failed_open.h5"
    # make it
    with open(uri, "wb") as junk:
        # out of text
        junk.write(b"this is not an h5 file" * 64)
    # attempt to open it; the failure leaves the file holding an empty handle
    f = libh5.File(uri=uri, mode="r")
    # and the library's reasons on its error stack, which name a file routine
    assert "H5F" in libh5.explanation()
    # the handle is one the library will not vouch for
    assert not libh5.valid(f.hid)
    # ask for the root, many times, so a stale answer on the stack gets its chance
    for _ in range(64):
        # there is nothing there
        assert f.get(path="/") is None
    # and there are no members
    assert f.members() == []
    # a file that is not there is refused the same way
    missing = libh5.File(uri="h5_ext_failed_open_missing.h5", mode="r")
    assert not libh5.valid(missing.hid)
    assert missing.get(path="/") is None
    assert missing.members() == []
    # clean up
    os.remove(uri)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
