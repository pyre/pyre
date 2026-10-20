#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the cfg codec refuses a file with a character it does not recognize
"""


def test():
    # package access
    import pyre.config

    # get the codec manager
    m = pyre.config.newConfigurator()
    # ask for a cfg codec
    reader = m.codec(encoding="cfg")
    # the configuration file
    uri = "sample-badToken.cfg"
    # open a stream
    sample = open(uri)
    # attempt to
    try:
        # read the contents
        reader.decode(uri=uri, source=sample, locator=None)
        # which should fail
        assert False
    # with a decoding error
    except reader.DecodingError as error:
        # about my file
        assert error.uri == uri
        # that carries what the parser found wrong with it
        assert error.errors

    return m, reader


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
