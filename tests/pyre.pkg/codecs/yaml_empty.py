#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


"""
Verify that we can process an empty {yaml} file
"""


def test():
    # package access
    import pyre.config
    # get the codec manager
    m = pyre.config.newConfigurator()
    # ask for a {yaml} codec
    reader = m.codec(encoding="yaml")
    # the configuration file
    uri = "sample-empty.yaml"
    # open a stream
    sample = open(uri)
    # read the contents
    events = reader.decode(uri=uri, source=sample, locator=None)
    # check that we got a real instance back
    assert tuple(events) == ()

    return m, reader, events


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
