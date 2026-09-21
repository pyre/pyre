#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a file the library would not open says so, rather than handing back a hole

An open that fails leaves the file holding an empty handle instead of raising, and the
library reports its reasons on an error stack the caller never sees. Whoever walks that
handle gets an attribute error about a {NoneType}, which names neither the product nor
anything that could be done about it
"""


# the driver
def test():
    # support
    import journal
    import pyre
    import pyre.h5

    # the local exceptions
    exceptions = pyre.h5.api.exceptions

    # the library prints a stack of its own on every failed open; it is not what is being
    # tested here, and it is not what the caller is told
    journal.error("pyre.h5.reader").device = journal.trash()

    # a product that is not there
    try:
        # cannot be read
        pyre.h5.reader(uri="access_errors_missing.h5").read()
    # and the refusal names it
    except exceptions.OpenError as error:
        assert "access_errors_missing.h5" in str(error)
    # anything else is a failure
    else:
        assert False, "a missing product was opened"

    # a file that is not h5 at all
    with open("access_errors_junk.h5", "wb") as junk:
        junk.write(b"this is not an h5 file" * 64)
    try:
        # is refused the same way
        pyre.h5.reader(uri="access_errors_junk.h5").read()
    # naming the file rather than the path
    except exceptions.OpenError as error:
        assert "access_errors_junk.h5" in str(error)
    else:
        assert False, "a file that is not h5 was opened"

    # a writer pointed at a directory has nowhere to put a product
    try:
        # so the write is refused before anything is traversed
        pyre.h5.writer(uri=".").write(query=pyre.h5.schema.group(name="root"))
    # by the same refusal, since the failure is the open
    except exceptions.OpenError:
        pass
    else:
        assert False, "a product was written into a directory"

    # a product that does open
    uri = pyre.primitives.path("access_errors.h5")
    pyre.h5.writer(uri=uri, mode="w").write(query=pyre.h5.schema.group(name="root"))
    assert uri.exists()
    # can be read at its root
    assert pyre.h5.reader(uri=uri).read() is not None
    # but asking it for something it does not hold is a different complaint, since the
    # file is fine and it is the path that is wrong
    try:
        # so it names the path
        pyre.h5.reader(uri=uri).read(path="/nowhere/at/all")
    except exceptions.PathError as error:
        assert "/nowhere/at/all" in str(error)
        assert str(uri) in str(error)
    else:
        assert False, "a product answered for a path it does not hold"

    # both refusals are h5 api errors, so a client that catches the family catches these
    assert issubclass(exceptions.OpenError, exceptions.APIError)
    assert issubclass(exceptions.PathError, exceptions.APIError)

    # a product in a bucket names the uri that was written, not the endpoint the driver
    # was handed; the rewritten address points at a host nobody typed
    if pyre.h5.libh5.ros3():
        # so reach for a bucket with keys that cannot open anything
        try:
            pyre.h5.reader(
                uri="s3://pyre-no-such-bucket/no-such-product.h5",
                credentials={
                    "region": "us-west-2",
                    "access_key": "AKIANOTREAL",
                    "secret_key": "notreal",
                    "token": "",
                },
            ).read()
        # and check that the complaint is about what the caller wrote
        except exceptions.OpenError as error:
            assert "s3://pyre-no-such-bucket/no-such-product.h5" in str(error)
        else:
            assert False, "a product in an unreachable bucket was opened"

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
