#! /usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Structural problems with a header are reported as exceptions that say where they are
    """
    # access the package
    import pyre

    # for headers in memory
    import io

    # the reader
    reader = pyre.envi.reader()
    # the exceptions
    exceptions = pyre.envi.exceptions

    # a file that does not open with the marker is not an ENVI header
    try:
        # parse
        reader.parse(stream=io.StringIO("samples = 10\n"), uri="memory")
    # the refusal
    except exceptions.MissingMarkerError as error:
        # names the source
        assert error.uri == "memory"
        assert "memory" in str(error)
    # anything else
    else:
        # is a failure
        assert False, "a header without the marker was accepted"

    # and neither is an empty file, or one with only comments
    try:
        # parse
        reader.parse(stream=io.StringIO("; nothing here\n\n"), uri="memory")
    # the refusal
    except exceptions.MissingMarkerError:
        # is expected
        pass
    # anything else
    else:
        # is a failure
        assert False, "an empty header was accepted"

    # a line that is not an assignment
    text = "ENVI\nsamples = 10\nthis is not an entry\n"
    try:
        # parse
        reader.parse(stream=io.StringIO(text), uri="memory")
    # the refusal
    except exceptions.MalformedHeaderError as error:
        # points at the line
        assert error.line == 3
        assert error.text == "this is not an entry"
        assert "line 3" in str(error)
    # anything else
    else:
        # is a failure
        assert False, "a line without an assignment was accepted"

    # a brace that is never closed
    text = "ENVI\nsamples = 10\nband names = {Band 1,\nBand 2\n"
    try:
        # parse
        reader.parse(stream=io.StringIO(text), uri="memory")
    # the refusal
    except exceptions.MalformedHeaderError as error:
        # points at the line that opened the brace
        assert error.line == 3
        assert error.reason == "unterminated brace"
    # anything else
    else:
        # is a failure
        assert False, "an unterminated brace was accepted"

    # a data type code ENVI does not define is caught by the trait validator on the way in, so
    # it lands in the extras; the datatype lookup itself refuses an unknown code
    hdr = pyre.envi.header()
    hdr.dataType = 12
    assert hdr.datatype == "uint16"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
