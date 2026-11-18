#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the driver
def test():
    """
    Verify that a file the library would not open says so, rather than handing back a hole

    An open that fails leaves the file holding an empty handle instead of raising, and the
    library reports its reasons on an error stack the caller never sees. Whoever walks that
    handle gets an attribute error about a {NoneType}, which names neither the product nor
    anything that could be done about it
    """
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
    # and the refusal
    except exceptions.OpenError as error:
        # names it
        assert "access_errors_missing.h5" in str(error)
    # anything else
    else:
        # is a failure
        assert False, "a missing product was opened"

    # a file that is not h5 at all
    with open("access_errors_junk.h5", "wb") as junk:
        # holds nothing but text
        junk.write(b"this is not an h5 file" * 64)
    # and
    try:
        # is refused the same way
        pyre.h5.reader(uri="access_errors_junk.h5").read()
    # by a refusal that
    except exceptions.OpenError as error:
        # names the file rather than the path
        assert "access_errors_junk.h5" in str(error)
    # anything else
    else:
        # is a failure
        assert False, "a file that is not h5 was opened"

    # a writer pointed at a directory has nowhere to put a product
    try:
        # so the write is refused before anything is traversed
        pyre.h5.writer(uri=".").write(query=pyre.h5.schema.group(name="root"))
    # by the same refusal, since the failure is the open
    except exceptions.OpenError:
        # which is what we expect
        pass
    # anything else
    else:
        # is a failure
        assert False, "a product was written into a directory"

    # a product that does open
    uri = pyre.primitives.path("access_errors.h5")
    # gets written
    pyre.h5.writer(uri=uri, mode="w").write(query=pyre.h5.schema.group(name="root"))
    # and lands on disk
    assert uri.exists()
    # it can be read at its root
    assert pyre.h5.reader(uri=uri).read() is not None
    # but asking it for something it does not hold is a different complaint, since the
    # file is fine and it is the path that is wrong
    try:
        # so ask for a path it does not hold
        pyre.h5.reader(uri=uri).read(path="/nowhere/at/all")
    # the refusal
    except exceptions.PathError as error:
        # names the path
        assert "/nowhere/at/all" in str(error)
        # and the product
        assert str(uri) in str(error)
    # anything else
    else:
        # is a failure
        assert False, "a product answered for a path it does not hold"

    # both refusals are h5 api errors, so a client that catches the family catches the
    # failed open
    assert issubclass(exceptions.OpenError, exceptions.APIError)
    # and the missing path
    assert issubclass(exceptions.PathError, exceptions.APIError)

    # a product in a bucket names the uri that was written, not the endpoint the driver
    # was handed; the rewritten address points at a host nobody typed
    if pyre.h5.libh5.ros3():
        # so reach for a bucket with keys that cannot open anything
        try:
            # and attempt to read from it
            pyre.h5.reader(
                uri="s3://pyre-no-such-bucket/no-such-product.h5",
                credentials={
                    "region": "us-west-2",
                    "access_key": "AKIANOTREAL",
                    "secret_key": "notreal",
                    "token": "",
                },
            ).read()
        # and check that the complaint
        except exceptions.OpenError as error:
            # is about what the caller wrote
            assert "s3://pyre-no-such-bucket/no-such-product.h5" in str(error)
        # anything else
        else:
            # is a failure
            assert False, "a product in an unreachable bucket was opened"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
